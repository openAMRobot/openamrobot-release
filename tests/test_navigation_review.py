"""Regression checks for PR #9's navigation-only scope and tool provenance."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('nav_install', ROOT / 'scripts/validate_navigation_install.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class NavigationReviewTests(unittest.TestCase):
    def test_config_is_navigation_only_without_rc_version(self):
        config = json.loads((ROOT / 'navigation-install-test-config.json').read_text())
        self.assertEqual(config['product']['name'], 'NavigationInstallTest')
        self.assertNotIn('rc', config['product']['version'])
        self.assertEqual([entry['id'] for entry in config['components']], ['interfaces'])
        self.assertFalse((ROOT / 'release-config.nav-install.json').exists())

    def test_tool_provenance_references_current_commit_and_sources(self):
        with patch.object(runner.subprocess, 'check_output', side_effect=['a' * 40 + '\n', '']):
            source = runner.verification_source(ROOT)
        self.assertEqual(source['commit'], 'a' * 40)
        self.assertFalse(source['working_tree_modified'])
        self.assertIn('scripts/nav-install/consumer.sh', source['files'])
        self.assertIn('scripts/nav-install/nav_consumer/smoke.cpp', source['files'])
        for name, digest in source['files'].items():
            self.assertEqual(digest, runner.digest(ROOT / name))

    def test_modified_tools_are_disclosed(self):
        with patch.object(runner.subprocess, 'check_output', side_effect=['a' * 40 + '\n', ' M scripts/nav-install/consumer.sh']):
            self.assertTrue(runner.verification_source(ROOT)['working_tree_modified'])
