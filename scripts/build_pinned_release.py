"""Build an immutable source bundle; legacy v0.0.1 builder remains available."""
import argparse
import hashlib
import io
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

import yaml


class StrictLoader(yaml.SafeLoader):
    pass


def mapping(loader, node):
    result = {}
    for key, value in node.value:
        key = loader.construct_object(key)
        if key in result:
            raise ValueError(f'duplicate key: {key}')
        result[key] = loader.construct_object(value)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    path = PurePosixPath(value)
    if not value or any(ord(c) < 32 for c in value) or path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value or str(path) != value:
        raise ValueError(f'unsafe path: {value}')
    return value


def load_manifest(path):
    data = yaml.load(path.read_text(encoding='utf-8'), Loader=StrictLoader)
    if not isinstance(data, dict) or set(data) != {'repositories'}:
        raise ValueError('expected repositories mapping')
    repos = data['repositories']
    if not isinstance(repos, dict) or not repos:
        raise ValueError('empty repositories')
    for name, entry in repos.items():
        safe_path(name)
        if set(entry) != {'type', 'url', 'version'} or entry['type'] != 'git':
            raise ValueError(f'{name}: expected git type, url, version')
        if not re.fullmatch(r'https://github.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?', entry['url']):
            raise ValueError(f'{name}: expected GitHub HTTPS URL')
        if not re.fullmatch(r'[0-9a-f]{40}', entry['version']):
            raise ValueError(f'{name}: full commit SHA required')
        if any(other != name and other.startswith(name + '/') for other in repos):
            raise ValueError('nested repository paths')
    return repos


def source_archive(entry):
    # Export directly from a verified tree, with conversion settings pinned below.
    # Archive bytes are generated from a verified Git commit, never main.zip.
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['git', 'init', '-q', tmp], check=True)
        subprocess.run(['git', '-C', tmp, 'fetch', '--depth=1', entry['url'], entry['version']], check=True)
        actual = subprocess.check_output(['git', '-C', tmp, 'rev-parse', 'FETCH_HEAD^{commit}'], text=True).strip()
        if actual != entry['version']:
            raise ValueError('fetched SHA mismatch')
        tree = subprocess.check_output(['git', '-C', tmp, 'ls-tree', '-r', actual], text=True)
        if any(line.startswith('160000 ') for line in tree.splitlines()):
            raise ValueError('submodules need explicit manifest entries')
        # Git archive applies checkout line-ending conversion. Pin these
        # settings so a Windows user's autocrlf does not change source bytes.
        data = subprocess.check_output([
            'git', '-C', tmp, '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
            'archive', '--format=zip', actual])
        return canonical_source(data)


def canonical_source(data):
    """Remove Git/zlib/platform ZIP metadata from the source checksum input."""
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(data)) as source, zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as dest:
        dest.comment = source.comment
        seen = set()
        for item in sorted(source.infolist(), key=lambda item: item.filename):
            if item.is_dir():
                continue
            name = safe_path(item.filename)
            if name in seen:
                raise ValueError('duplicate source member')
            seen.add(name)
            mode = item.external_attr >> 16
            mode = 0o120777 if mode & 0o170000 == 0o120000 else (0o100755 if mode & 0o111 else 0o100644)
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = mode << 16
            dest.writestr(info, source.read(item))
    return output.getvalue()


def write_zip(path, files):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, (data, mode) in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, data)


def validate(path):
    """Verify inventory coverage and every member without extracting symlinks."""
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('duplicate archive member')
        for name in names:
            safe_path(name)
        expected = {}
        for line in archive.read('checksums.sha256').decode().splitlines():
            checksum, name = line.split('  ', 1)
            safe_path(name)
            if name in expected or not re.fullmatch(r'[0-9a-f]{64}', checksum):
                raise ValueError('invalid checksum inventory')
            expected[name] = checksum
        if set(names) != set(expected) | {'checksums.sha256'}:
            raise ValueError('inventory coverage mismatch')
        for name, checksum in expected.items():
            if digest(archive.read(name)) != checksum:
                raise ValueError(f'checksum mismatch: {name}')
        metadata = json.loads(archive.read('MANIFEST.json'))
        if digest(archive.read('release.repos')) != metadata['manifest_sha256']:
            raise ValueError('manifest checksum mismatch')
        print(f'PASS: {len(expected)} files verified')


def build(config_path, output, cache, fetch=False):
    config = json.loads(config_path.read_text(encoding='utf-8'))
    manifest_path = config_path.parent / config['manifest']
    manifest_bytes = manifest_path.read_bytes()
    if digest(manifest_bytes) != config['manifest_sha256']:
        raise ValueError('manifest checksum mismatch')
    repos = load_manifest(manifest_path)
    if set(config['sources']) != set(repos):
        raise ValueError('source checksum coverage mismatch')
    files = {'release.repos': (manifest_bytes, 0o100644)}
    components = []
    cache.mkdir(parents=True, exist_ok=True)
    for name, entry in repos.items():
        expected = config['sources'][name]
        if not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise ValueError(f'{name}: SHA256 required')
        cached = cache / (expected + '.zip')
        if fetch:
            data = source_archive(entry)
            if digest(data) != expected:
                raise ValueError(f'{name}: source checksum mismatch: expected {expected}, got {digest(data)}')
            cached.write_bytes(data)
        data = cached.read_bytes()
        if digest(data) != expected:
            raise ValueError(f'{name}: source checksum mismatch')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if archive.comment.decode('ascii') != entry['version']:
                raise ValueError(f'{name}: archive commit mismatch')
            for item in archive.infolist():
                if item.is_dir():
                    continue
                rel = safe_path(item.filename)
                mode = (item.external_attr >> 16) & 0o170777
                if mode & 0o170000 == 0o120000:
                    # Preserve link bytes and mode without following the target.
                    mode = 0o120777
                else:
                    mode = 0o100755 if mode & 0o111 else 0o100644
                files[name + '/' + rel] = (archive.read(item), mode)
        components.append(dict(path=name, **entry, archive_sha256=expected))
    metadata = {'product': config['product'], 'manifest_sha256': digest(manifest_bytes), 'components': components}
    files['MANIFEST.json'] = ((json.dumps(metadata, indent=2, sort_keys=True) + '\n').encode(), 0o100644)
    checksums = ''.join(f'{digest(data)}  {name}\n' for name, (data, _) in sorted(files.items()))
    files['checksums.sha256'] = (checksums.encode(), 0o100644)
    output.mkdir(parents=True, exist_ok=True)
    version = config['product']['version']
    if not re.fullmatch(r'[0-9A-Za-z.-]+', version):
        raise ValueError('invalid product version')
    target = output / f'OpenAMRobot-v{version}-source.zip'
    write_zip(target, files)
    validate(target)
    target.with_suffix('.zip.sha256').write_text(f'{digest(target.read_bytes())}  {target.name}\n', encoding='ascii')
    print(f'{target}: {digest(target.read_bytes())}')
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--fetch', action='store_true', help='fetch and verify every source by SHA')
    args = parser.parse_args()
    build(args.config, args.output_dir, args.cache_dir, args.fetch)
