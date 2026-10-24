"""Exercise release builder acceptance and rejection with pinned archive evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SHA = 'a' * 40


class NavigationManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'input').mkdir()
        (self.root / 'metadata').mkdir()
        (self.root / 'metadata/README.md').write_text('test fixture\n')
        self.archive = self.root / 'input/interfaces.zip'
        with zipfile.ZipFile(self.archive, 'w') as archive:
            archive.comment = SHA.encode()
            archive.writestr('interfaces/README.md', 'fixture')
            archive.writestr('interfaces/ros2/openamr_nav_msgs/package.xml', '<package><version>0.0.0</version></package>')
            archive.writestr('interfaces/ros2/openamr_nav_msgs/msg/NavigationStatus.msg', 'uint16 CONTRACT_VERSION=1\n')
        self.manifest = {
            'source_commit': SHA, 'packages': {'openamr_nav_msgs': '0.0.0'},
            'contract_version': 1, 'validation_image': 'ros@sha256:' + 'b' * 64,
            'platform': 'linux/amd64', 'status': 'source-install-candidate',
            'evidence_path': 'result.json',
        }
        self.evidence = dict(self.manifest, status='passed', runs=[{
            'source_archive_sha256': hashlib.sha256(self.archive.read_bytes()).hexdigest(),
            'install_artifact_sha256': 'c' * 64,
        }])
        config = {
            'product': {'name': 'Fixture', 'version': '0.0.0'},
            'components': [{'id': 'interfaces', 'archive': 'interfaces.zip',
                            'expected_root': 'interfaces', 'destination': '06_Interfaces',
                            'repository': 'https://github.com/openAMRobot/openamrobot-interfaces',
                            'install_manifest': 'install.json'}],
            'required_paths': ['MANIFEST.json'],
        }
        (self.root / 'config.json').write_text(json.dumps(config))

    def build(self):
        (self.root / 'install.json').write_text(json.dumps(self.manifest))
        (self.root / 'result.json').write_text(json.dumps(self.evidence))
        return subprocess.run([
            sys.executable, str(ROOT / 'scripts/build_release.py'),
            '--config', str(self.root / 'config.json'), '--input-dir', str(self.root / 'input'),
            '--output-dir', str(self.root / 'out'), '--metadata-dir', str(self.root / 'metadata'),
        ], capture_output=True, text=True)

    def test_validated_pin_and_contract_reach_product_manifest(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.root / 'out/Fixture-v0.0.0-source.zip') as archive:
            manifest = json.loads(archive.read('Fixture-v0.0.0/MANIFEST.json'))
        record = manifest['components'][0]
        self.assertEqual(record['source_commit'], SHA)
        self.assertEqual(record['packages'], {'openamr_nav_msgs': '0.0.0'})
        self.assertEqual(record['contract_version'], 1)
        self.assertEqual(record['installation_evidence']['runs'][0]['install_artifact_sha256'], 'c' * 64)

    def test_failed_install_is_rejected(self):
        self.evidence['status'] = 'failed'
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not passing', result.stderr)

    def test_different_evidence_pin_is_rejected(self):
        self.evidence['source_commit'] = 'd' * 40
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('evidence mismatch: source_commit', result.stderr)

    def test_different_archive_bytes_are_rejected(self):
        self.evidence['runs'][0]['source_archive_sha256'] = 'e' * 64
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not the archive validated', result.stderr)

    def test_wrong_archive_commit_is_rejected(self):
        with zipfile.ZipFile(self.archive, 'a') as archive:
            archive.comment = ('f' * 40).encode()
        self.evidence['runs'][0]['source_archive_sha256'] = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('archive commit does not match', result.stderr)

    def test_wrong_package_version_is_rejected(self):
        self.manifest['packages'] = {'openamr_nav_msgs': '9.9.9'}
        self.evidence['packages'] = self.manifest['packages']
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('package version does not match', result.stderr)

    def test_wrong_contract_version_is_rejected(self):
        self.manifest['contract_version'] = 2
        self.evidence['contract_version'] = 2
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('contract version does not match', result.stderr)

    def test_legacy_configuration_still_builds_without_install_evidence(self):
        path = self.root / 'config.json'
        config = json.loads(path.read_text())
        del config['components'][0]['install_manifest']
        path.write_text(json.dumps(config))
        self.evidence['status'] = 'failed'
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
