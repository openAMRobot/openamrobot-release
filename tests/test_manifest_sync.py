"""Parity must cover every workspace source, including the drivers."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_manifest_sync import check_sync


class ManifestSyncTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.entry = {'type': 'git', 'url': 'https://github.com/example/source.git',
                      'version': 'a' * 40}
        self.repos = {'src/example': self.entry, 'src/sllidar_ros2': self.entry}

    def write(self, name, repos):
        path = self.root / name
        path.write_text(yaml.safe_dump({'repositories': repos}), encoding='utf-8')
        return path

    def compare(self, release, workspace):
        return check_sync(self.write('release.repos', release),
                          self.write('workspace.repos', workspace))

    def test_order_and_comments_do_not_matter(self):
        release = self.write('release.repos', self.repos)
        workspace = self.root / 'workspace.repos'
        workspace.write_text('# workspace\n' + yaml.safe_dump(
            {'repositories': dict(reversed(list(self.repos.items())))},
            sort_keys=False), encoding='utf-8')
        self.assertEqual(check_sync(release, workspace), 2)

    def test_only_governance_is_exempt(self):
        release = dict(self.repos, **{'governance/.github': self.entry})
        self.assertEqual(self.compare(release, self.repos), 2)

    def test_missing_driver_fails(self):
        with self.assertRaisesRegex(ValueError, 'src/sllidar_ros2: missing'):
            self.compare(self.repos, {'src/example': self.entry})

    def test_missing_release_entry_fails(self):
        with self.assertRaisesRegex(ValueError, 'missing from release'):
            self.compare({'src/example': self.entry}, self.repos)

    def test_changed_sha_or_url_fails(self):
        for field, value in [('version', 'b' * 40),
                             ('url', 'https://github.com/example/other.git')]:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.repos)
                changed['src/example'][field] = value
                with self.assertRaisesRegex(ValueError, 'differs'):
                    self.compare(self.repos, changed)

    def test_missing_reference_fails(self):
        with self.assertRaises(FileNotFoundError):
            check_sync(self.write('release.repos', self.repos), self.root / 'absent')

    def test_mutable_reference_fails(self):
        changed = copy.deepcopy(self.repos)
        changed['src/example']['version'] = 'main'
        with self.assertRaisesRegex(ValueError, 'full commit SHA required'):
            self.compare(self.repos, changed)
