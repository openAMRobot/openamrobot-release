#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, os, shutil, sys, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def copy_tree(src: Path, dst: Path, excluded: set[str]) -> None:
    def ignore(_dir, names):
        return [n for n in names if n in excluded]
    shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=True)


def zip_tree(source_dir: Path, output_zip: Path) -> None:
    with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as zf:
        for path in sorted(source_dir.rglob('*')):
            if path.is_file():
                zf.write(path, path.relative_to(source_dir.parent))


def main() -> int:
    p = argparse.ArgumentParser(description='Build a frozen multi-repository OpenAMRobot product release.')
    p.add_argument('--config', required=True, type=Path)
    p.add_argument('--input-dir', required=True, type=Path)
    p.add_argument('--output-dir', required=True, type=Path)
    p.add_argument('--metadata-dir', type=Path, default=Path('release-metadata'))
    p.add_argument('--keep-staging', action='store_true')
    args = p.parse_args()

    cfg = json.loads(args.config.read_text())
    product = cfg['product']
    version = product['version']
    package_name = f"{product['name']}-v{version}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    staging_parent = args.output_dir / '_staging'
    package_dir = staging_parent / package_name
    if staging_parent.exists(): shutil.rmtree(staging_parent)
    package_dir.mkdir(parents=True)

    metadata = args.metadata_dir
    if not metadata.is_dir():
        raise SystemExit(f'Metadata directory not found: {metadata}')
    for file in metadata.iterdir():
        if file.is_file(): shutil.copy2(file, package_dir / file.name)
    (package_dir/'01_Getting_Started').mkdir()
    if (metadata/'RELEASE_SCOPE.md').exists():
        shutil.copy2(metadata/'RELEASE_SCOPE.md', package_dir/'01_Getting_Started/RELEASE_SCOPE.md')

    manifest = {
        'product': product,
        'built_at_utc': datetime.now(timezone.utc).isoformat(),
        'builder': 'OpenAMRobot Release Builder',
        'components': []
    }
    excluded = set(cfg.get('exclude_names', []))

    for component in cfg['components']:
        archive = args.input_dir / component['archive']
        if not archive.is_file():
            raise SystemExit(f"Missing component archive: {archive}")
        archive_hash = sha256(archive)
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(td_path)
                comment = zf.comment.decode('utf-8', errors='replace').strip()
            root = td_path / component['expected_root']
            if not root.is_dir():
                roots = [x.name for x in td_path.iterdir()]
                raise SystemExit(f"Expected root {component['expected_root']} not found in {archive.name}; found {roots}")
            destination = package_dir / component['destination']
            copy_tree(root, destination, excluded)
        manifest['components'].append({
            'id': component['id'],
            'repository': component['repository'],
            'archive': archive.name,
            'archive_sha256': archive_hash,
            'source_archive_comment_or_commit': comment or None,
            'destination': component['destination']
        })

    (package_dir/'VERSION').write_text(version+'\n')
    (package_dir/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')

    # File inventory and internal checksums
    inventory_path = args.output_dir / f'{package_name}-inventory.csv'
    checksum_lines = []
    with inventory_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['path','size_bytes','sha256'])
        for path in sorted(package_dir.rglob('*')):
            if path.is_file() and path.name != 'checksums.sha256':
                rel = path.relative_to(package_dir).as_posix()
                digest = sha256(path)
                w.writerow([rel, path.stat().st_size, digest])
                checksum_lines.append(f'{digest}  {rel}')
    (package_dir/'checksums.sha256').write_text('\n'.join(checksum_lines)+'\n')

    missing = [x for x in cfg.get('required_paths', []) if not (package_dir/x).exists()]
    report = [f'# Build report — {package_name}', '', f'- Components: {len(cfg["components"])}', f'- Files: {sum(1 for p in package_dir.rglob("*") if p.is_file())}', f'- Package size before ZIP: {sum(p.stat().st_size for p in package_dir.rglob("*") if p.is_file())} bytes', '']
    if missing:
        report += ['## FAILED: missing required paths', *[f'- `{x}`' for x in missing]]
    else:
        report += ['## PASS: required paths present']
    (args.output_dir/'build-report.md').write_text('\n'.join(report)+'\n')
    if missing:
        return 2

    output_zip = args.output_dir / f'{package_name}-source.zip'
    if output_zip.exists(): output_zip.unlink()
    zip_tree(package_dir, output_zip)
    zip_hash = sha256(output_zip)
    (args.output_dir/f'{output_zip.name}.sha256').write_text(f'{zip_hash}  {output_zip.name}\n')

    if not args.keep_staging:
        shutil.rmtree(staging_parent)
    print(output_zip)
    print(f'SHA256: {zip_hash}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
