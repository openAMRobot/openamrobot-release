"""Prepare a candidate checksum lock from a reviewed SHA-only manifest."""
import argparse
import json
from pathlib import Path
from build_pinned_release import digest, load_manifest, source_archive

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    # Keep review of a new lock explicit: never replace an existing lock file.
    if args.output.exists():
        raise SystemExit('Choose a new output file; existing locks are not overwritten')
    relative = args.manifest.resolve().relative_to(args.output.parent.resolve()).as_posix()
    repos = load_manifest(args.manifest)
    config = {'product': {'name': 'OpenAMRobot', 'version': args.version,
                          'status': 'candidate snapshot; not release acceptance'},
              'manifest': relative, 'manifest_sha256': digest(args.manifest.read_bytes()), 'sources': {}}
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    for name, entry in repos.items():
        data = source_archive(entry)
        checksum = digest(data)
        (args.cache_dir / (checksum + '.zip')).write_bytes(data)
        config['sources'][name] = checksum
        print(f'{name}: {entry["version"]} {checksum}', flush=True)
    args.output.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8', newline='\n')
