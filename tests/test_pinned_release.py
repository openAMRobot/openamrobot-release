"""Offline fault injection and reproducibility tests for rc.1 packaging."""
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_pinned_release as builder


class PinnedReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sha = 'a' * 40
        self.entry = {'type': 'git', 'url': 'https://github.com/example/source.git', 'version': self.sha}
        self.manifest = self.root / 'release.repos'
        self.manifest.write_text(yaml.safe_dump({'repositories': {'src/example': self.entry}}))
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive:
            archive.comment = self.sha.encode()
            archive.writestr('README.md', b'source content\n')
        self.source = data.getvalue()
        self.checksum = builder.digest(self.source)
        self.cache = self.root / 'cache'
        self.cache.mkdir()
        (self.cache / (self.checksum + '.zip')).write_bytes(self.source)
        self.config = {'product': {'name': 'OpenAMRobot', 'version': '2.0.0-rc.1'},
                       'manifest': 'release.repos', 'manifest_sha256': builder.digest(self.manifest.read_bytes()),
                       'sources': {'src/example': self.checksum}}
        self.config_path = self.root / 'config.json'
        self.save_config()

    def save_config(self):
        self.config_path.write_text(json.dumps(self.config))

    def build(self, name='out', fetch=False):
        return builder.build(self.config_path, self.root / name, self.cache, fetch)

    def test_two_builds_identical(self):
        first = self.build('first')
        second = self.build('second')
        self.assertEqual(first.read_bytes(), second.read_bytes())
        builder.validate(first)
        with zipfile.ZipFile(first) as archive:
            component = json.loads(archive.read('MANIFEST.json'))['components'][0]
            self.assertEqual(component['version'], self.sha)
            self.assertEqual(component['archive_sha256'], self.checksum)

    def test_source_normalization_ignores_zip_metadata(self):
        variants = []
        for date, compression in (((2001, 1, 1, 0, 0, 0), zipfile.ZIP_STORED),
                                  ((2026, 1, 1, 0, 0, 0), zipfile.ZIP_DEFLATED)):
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w', compression=compression) as archive:
                archive.comment = self.sha.encode()
                item = zipfile.ZipInfo('README.md', date_time=date)
                item.compress_type = compression
                item.external_attr = 0o100644 << 16
                archive.writestr(item, b'same bytes')
            variants.append(builder.canonical_source(stream.getvalue()))
        self.assertEqual(*variants)

    def test_source_hash_ignores_git_line_ending_defaults(self):
        revision = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
        entry = {'url': str(ROOT), 'version': revision}
        hashes = []
        for autocrlf in ('true', 'false'):
            with patch.dict(os.environ, {'GIT_CONFIG_COUNT': '1',
                                        'GIT_CONFIG_KEY_0': 'core.autocrlf',
                                        'GIT_CONFIG_VALUE_0': autocrlf}):
                hashes.append(builder.digest(builder.source_archive(entry)))
        self.assertEqual(hashes[0], hashes[1])

    def test_executable_and_symlink_modes_preserved(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive:
            for name, mode, content in [('tool.sh', 0o100755, b'echo test'),
                                        ('link', 0o120777, b'tool.sh')]:
                item = zipfile.ZipInfo(name)
                item.external_attr = mode << 16
                archive.writestr(item, content)
        normalized = builder.canonical_source(data.getvalue())
        with zipfile.ZipFile(io.BytesIO(normalized)) as archive:
            self.assertEqual(archive.getinfo('tool.sh').external_attr >> 16, 0o100755)
            self.assertEqual(archive.getinfo('link').external_attr >> 16, 0o120777)
            self.assertEqual(archive.read('link'), b'tool.sh')

    def test_fetch_uses_full_sha_and_verifies_commit(self):
        outputs = [self.sha + '\n', '', self.source]
        with patch.object(builder.subprocess, 'run') as run, patch.object(builder.subprocess, 'check_output', side_effect=outputs):
            self.assertEqual(builder.source_archive(self.entry), builder.canonical_source(self.source))
            fetch_args = run.call_args_list[1].args[0]
            self.assertEqual(fetch_args[-2:], [self.entry['url'], self.sha])

    def test_fetched_wrong_sha_and_submodules_rejected(self):
        with patch.object(builder.subprocess, 'run'), patch.object(builder.subprocess, 'check_output', return_value='b' * 40):
            with self.assertRaisesRegex(ValueError, 'fetched SHA mismatch'):
                builder.source_archive(self.entry)
        with patch.object(builder.subprocess, 'run'), patch.object(builder.subprocess, 'check_output', side_effect=[self.sha, '160000 commit deadbeef\tsubmodule']):
            with self.assertRaisesRegex(ValueError, 'submodules'):
                builder.source_archive(self.entry)

    def test_changed_manifest_rejected(self):
        self.manifest.write_text(self.manifest.read_text() + '# changed\n')
        with self.assertRaisesRegex(ValueError, 'manifest checksum mismatch'):
            self.build()

    def test_branch_tag_and_short_sha_rejected(self):
        for version in ('main', 'v2.0.0-rc.1', self.sha[:7]):
            with self.subTest(version=version):
                self.entry['version'] = version
                self.manifest.write_text(yaml.safe_dump({'repositories': {'src/example': self.entry}}))
                with self.assertRaisesRegex(ValueError, 'full commit SHA'):
                    builder.load_manifest(self.manifest)

    def test_duplicate_manifest_keys_rejected(self):
        self.manifest.write_text('repositories: {}\nrepositories: {}\n')
        with self.assertRaisesRegex(ValueError, 'duplicate key'):
            builder.load_manifest(self.manifest)

    def test_tampered_cached_source_rejected(self):
        (self.cache / (self.checksum + '.zip')).write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'source checksum mismatch'):
            self.build()

    def test_fetch_mismatch_rejected(self):
        with patch.object(builder, 'source_archive', return_value=b'wrong source'):
            with self.assertRaisesRegex(ValueError, 'source checksum mismatch'):
                self.build(fetch=True)

    def test_wrong_archive_commit_rejected(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive:
            archive.comment = ('b' * 40).encode()
            archive.writestr('README.md', 'wrong commit')
        raw = data.getvalue()
        checksum = builder.digest(raw)
        (self.cache / (checksum + '.zip')).write_bytes(raw)
        self.config['sources']['src/example'] = checksum
        self.save_config()
        with self.assertRaisesRegex(ValueError, 'archive commit mismatch'):
            self.build()

    def test_missing_checksum_rejected(self):
        self.config['sources'] = {}
        self.save_config()
        with self.assertRaisesRegex(ValueError, 'coverage mismatch'):
            self.build()

    def test_output_tampering_and_extra_file_rejected(self):
        original = self.build()
        for mutation in ('content', 'extra'):
            with self.subTest(mutation=mutation):
                target = self.root / (mutation + '.zip')
                with zipfile.ZipFile(original) as source, zipfile.ZipFile(target, 'w') as dest:
                    for name in source.namelist():
                        data = source.read(name)
                        if mutation == 'content' and name == 'src/example/README.md':
                            data = b'tampered'
                        dest.writestr(name, data)
                    if mutation == 'extra':
                        dest.writestr('extra.txt', b'extra')
                with self.assertRaisesRegex(ValueError, 'checksum mismatch|coverage mismatch'):
                    builder.validate(target)

    def test_unsafe_paths_rejected(self):
        for path in ('../escape', '/absolute', 'C:/escape', 'a\\b', 'a\nb', 'a/../b'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'unsafe path'):
                builder.safe_path(path)

    def test_existing_cli_dispatches_rc1(self):
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_release.py'), '--config', str(self.config_path),
                        '--input-dir', str(self.cache), '--output-dir', str(self.root / 'cli')], check=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/validate_release.py'),
                        str(self.root / 'cli/OpenAMRobot-v2.0.0-rc.1-source.zip')], check=True)

    def test_legacy_v001_build_and_validation_unchanged(self):
        config = json.loads((ROOT / 'release-config.json').read_text())
        inputs = self.root / 'legacy-input'
        inputs.mkdir()
        for component in config['components']:
            with zipfile.ZipFile(inputs / component['archive'], 'w') as archive:
                archive.writestr(component['expected_root'] + '/README.md', 'legacy fixture')
        output = self.root / 'legacy-output'
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_release.py'),
                        '--config', str(ROOT / 'release-config.json'), '--input-dir', str(inputs),
                        '--output-dir', str(output), '--metadata-dir', str(ROOT / 'release-metadata')], check=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/validate_release.py'),
                        str(output / 'OpenAMRobot-v0.0.1-source.zip')], check=True)


if __name__ == '__main__':
    unittest.main()
