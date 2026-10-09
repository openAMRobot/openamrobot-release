#!/usr/bin/env python3
"""Validate the release manifest pin in independent producer/consumer containers."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=Path('navigation-install-manifest.json'))
    parser.add_argument('--evidence', required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    revision = manifest['source_commit']
    if len(revision) != 40 or any(c not in '0123456789abcdef' for c in revision):
        parser.error('source_commit must be a full lowercase commit SHA')
    if '@sha256:' not in manifest['validation_image']:
        parser.error('validation_image must be digest-pinned')
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    result = {
        'status': 'failed', 'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'source_commit': revision, 'packages': manifest['packages'],
        'contract_version': manifest['contract_version'],
        'validation_image': manifest['validation_image'], 'platform': manifest['platform'],
        'workflow_run_url': (f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
                             if os.environ.get('GITHUB_REPOSITORY') and os.environ.get('GITHUB_RUN_ID') else None),
        'runs': [],
    }
    shutil.copyfile(args.manifest, evidence / 'manifest.json')
    commands = []

    def run(command, log):
        commands.append({'argv': command, 'log': log.relative_to(evidence).as_posix()})
        (evidence / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        with log.open('w', encoding='utf-8') as output:
            subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, check=True)

    try:
        run(['docker', 'pull', '--platform', manifest['platform'], manifest['validation_image']], evidence / 'image-pull.log')
        # Snapshot finalized scripts; editing the working tree cannot change a running shell.
        with tempfile.TemporaryDirectory(prefix='openamrobot-nav-checks-') as temporary:
            checks = Path(temporary) / 'checks'
            shutil.copytree(Path(__file__).parent / 'nav-install', checks)
            shutil.copytree(checks, evidence / 'verification-tools')
            shutil.copyfile(__file__, evidence / 'verification-tools/validate_navigation_install.py')
            for attempt in ('first', 'second'):
                folder = evidence / attempt
                producer = folder / 'producer'
                consumer = folder / 'consumer'
                producer.mkdir(parents=True)
                consumer.mkdir()
                common = ['docker', 'run', '--rm', '--platform', manifest['platform'],
                          '--mount', f'type=bind,source={checks},target=/checks,readonly']
                print(f'{attempt}: build exact pin in a fresh producer container', flush=True)
                run(common + ['--mount', f'type=bind,source={producer},target=/evidence',
                              manifest['validation_image'], 'bash', '/checks/producer.sh',
                              manifest['source_repository'], revision, manifest['packages']['openamr_nav_msgs']],
                    producer / 'validation.log')
                with zipfile.ZipFile(producer / 'interfaces-source.zip') as archive:
                    if archive.comment.decode() != revision:
                        raise RuntimeError('Source archive commit does not match manifest pin')
                print(f'{attempt}: check installed artifact in a separate source-free consumer container', flush=True)
                run(common + ['--mount', f'type=bind,source={producer / "navigation-install.tar.gz"},target=/artifact/navigation-install.tar.gz,readonly',
                              '--mount', f'type=bind,source={consumer},target=/evidence',
                              manifest['validation_image'], 'bash', '/checks/consumer.sh', str(manifest['contract_version'])],
                    consumer / 'validation.log')
                result['runs'].append({
                    'name': attempt, 'status': 'passed',
                    'install_artifact': f'{attempt}/producer/navigation-install.tar.gz',
                    'install_artifact_sha256': digest(producer / 'navigation-install.tar.gz'),
                    'source_archive': f'{attempt}/producer/interfaces-source.zip',
                    'source_archive_sha256': digest(producer / 'interfaces-source.zip'),
                    'generated_messages_verified': 11, 'consumer_build_and_run': 'passed',
                    'absent_install_negative_control': 'passed',
                    'producer_source_available_to_consumer': False,
                })
        comparison = {}
        for stage, name in (('consumer', 'generated.sha256'), ('consumer', 'interfaces.txt'),
                            ('consumer', 'dependencies.txt'), ('producer', 'dependencies.txt')):
            first = evidence / 'first' / stage / name
            second = evidence / 'second' / stage / name
            if first.read_bytes() != second.read_bytes():
                raise RuntimeError(f'Clean installs differ: {stage}/{name}')
            comparison[f'{stage}/{name}'] = digest(first)
        result['comparison'] = comparison
        result['status'] = 'passed'
    except Exception as error:
        result['error'] = str(error)
        raise
    finally:
        result['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        (evidence / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        lines = [f'{digest(path)}  {path.relative_to(evidence).as_posix()}'
                 for path in sorted(evidence.rglob('*')) if path.is_file() and path.name != 'checksums.sha256']
        (evidence / 'checksums.sha256').write_text('\n'.join(lines) + '\n')
    print(f'PASS: two pinned installs, generated interfaces and independent consumers; {evidence}')


if __name__ == '__main__':
    main()
