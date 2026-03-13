from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, '-m', 'governance_sandbox.cli', 'run']

class TopLevelReportFileAliasesTests(unittest.TestCase):
    def test_top_level_report_file_aliases_write_report_bundle_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.json'
            json_path = tmp / 'artifacts' / 'alias-result.json'
            markdown_path = tmp / 'artifacts' / 'alias-result.md'
            html_path = tmp / 'artifacts' / 'alias-result.html'
            scenario_path.write_text(json.dumps({
                'proposal': 'Load one scenario file and generate one named report trio for reviewers.',
                'stakeholders': [{'name': 'DAO Council', 'preset': 'dao'}, {'name': 'Delegates', 'preset': 'delegates'}],
                'report_json_file': str(json_path),
                'report_md_file': str(markdown_path),
                'report_html_file': str(html_path),
            }), encoding='utf-8')
            completed = subprocess.run(CLI + ['--scenario-file', str(scenario_path)], cwd=ROOT, env={'PYTHONPATH': 'src'}, capture_output=True, text=True, check=True)
            payload = json.loads(completed.stdout)
            artifacts = payload['report']['artifacts']
            self.assertEqual(Path(artifacts['json']), json_path.resolve())
            self.assertEqual(Path(artifacts['markdown']), markdown_path.resolve())
            self.assertEqual(Path(artifacts['html']), html_path.resolve())
            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())

if __name__ == '__main__':
    unittest.main()
