from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, '-m', 'governance_sandbox.cli', 'run']


class TopLevelOutputMdPathAliasesTests(unittest.TestCase):
    def test_top_level_output_md_path_aliases_write_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.json'
            markdown_path = tmp / 'artifacts' / 'decision-memo.md'
            scenario_path.write_text(json.dumps({
                'proposal': 'Load one scenario file and point directly at a markdown report alias.',
                'stakeholders': [{'name': 'DAO Council', 'preset': 'dao'}],
                'output_md_path': str(markdown_path),
            }), encoding='utf-8')
            completed = subprocess.run(CLI + ['--scenario-file', str(scenario_path)], cwd=ROOT, env={'PYTHONPATH': 'src'}, capture_output=True, text=True, check=True)
            payload = json.loads(completed.stdout)
            artifacts = payload['report']['artifacts']
            self.assertEqual(Path(artifacts['markdown']), markdown_path.resolve())
            self.assertTrue(markdown_path.exists())

    def test_top_level_output_md_file_alias_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.json'
            markdown_path = tmp / 'artifacts' / 'decision-summary.md'
            scenario_path.write_text(json.dumps({
                'proposal': 'Load one scenario file and point directly at a markdown report file alias.',
                'stakeholders': [{'name': 'Delegates', 'preset': 'delegates'}],
                'output_md_file': str(markdown_path),
            }), encoding='utf-8')
            completed = subprocess.run(CLI + ['--scenario-file', str(scenario_path)], cwd=ROOT, env={'PYTHONPATH': 'src'}, capture_output=True, text=True, check=True)
            payload = json.loads(completed.stdout)
            artifacts = payload['report']['artifacts']
            self.assertEqual(Path(artifacts['markdown']), markdown_path.resolve())
            self.assertTrue(markdown_path.exists())


if __name__ == '__main__':
    unittest.main()
