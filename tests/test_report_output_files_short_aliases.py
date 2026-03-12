from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


class ReportOutputFilesShortAliasesTests(unittest.TestCase):
    def test_run_supports_report_outputs_files_short_report_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            scenario_path = tmp_path / 'scenario.json'
            scenario_path.write_text(json.dumps({
                'proposal': {
                    'title': 'Treasury diversification vote',
                    'summary': 'Shift 5% of idle treasury into short-duration bills.'
                },
                'stakeholders': [
                    {'name': 'Core delegate', 'preset': 'delegates'},
                    {'name': 'Forum contributor', 'preset': 'contributors'}
                ],
                'report': {
                    'outputs': {
                        'files': {
                            'json_report': 'artifacts/brief.json',
                            'markdown_report': 'artifacts/brief.md',
                            'html_report': 'artifacts/brief.html'
                        }
                    }
                }
            }), encoding='utf-8')

            result = subprocess.run([sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)], cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(SRC)}, capture_output=True, text=True, check=True)
            payload = json.loads(result.stdout)
            self.assertEqual(Path(payload['report']['artifacts']['json']).name, 'brief.json')
            self.assertEqual(Path(payload['report']['artifacts']['markdown']).name, 'brief.md')
            self.assertEqual(Path(payload['report']['artifacts']['html']).name, 'brief.html')
            self.assertTrue((tmp_path / 'artifacts' / 'brief.md').exists())
            self.assertTrue((tmp_path / 'artifacts' / 'brief.html').exists())
            self.assertTrue((tmp_path / 'artifacts' / 'brief.json').exists())


if __name__ == '__main__':
    unittest.main()
