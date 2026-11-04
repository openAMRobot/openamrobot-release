"""Reject unsupported expectations before contacting Docker or fetching source."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('repin_runner', ROOT / 'scripts/validate_navigation_install.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RepinExpectationsTests(unittest.TestCase):
    def reject(self, field, value):
        manifest = json.loads((ROOT / 'navigation-install-manifest.json').read_text())
        if field == 'package':
            manifest['packages']['openamr_nav_msgs'] = value
        else:
            manifest[field] = value
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'manifest.json'
            path.write_text(json.dumps(manifest))
            evidence = Path(tmp) / 'evidence'
            with patch.object(sys, 'argv', ['runner', '--manifest', str(path), '--evidence', str(evidence)]), \
                    patch.object(runner, 'verification_source', return_value={}), \
                    patch.object(runner.subprocess, 'run') as execute:
                with self.assertRaises(SystemExit) as error:
                    runner.main()
                self.assertEqual(error.exception.code, 2)
                execute.assert_not_called()
                self.assertFalse(evidence.exists())

    def test_unknown_contract_rejected_before_build(self):
        self.reject('contract_version', 3)

    def test_non_numeric_contract_rejected_before_build(self):
        self.reject('contract_version', '2')

    def test_mutable_package_expectation_rejected_before_build(self):
        self.reject('package', 'latest')
