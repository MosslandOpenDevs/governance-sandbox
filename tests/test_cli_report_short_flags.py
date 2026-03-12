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


class GovernanceSandboxCliReportShortFlagsTests(unittest.TestCase):
    def test_run_supports_short_report_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            markdown_path = tmp / 'report.md'
            html_path = tmp / 'report.html'
            scenario_path.write_text('proposal: Publish a staged treasury automation memo before execution.\nstakeholders:\n  - name: Delegate council\n    preset: delegates\n', encoding='utf-8')

            result = subprocess.run([sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path), '--report-md', str(markdown_path), '--report-htm', str(html_path)], cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(SRC)}, capture_output=True, text=True, check=True)

            payload = json.loads(result.stdout)
            self.assertEqual(payload['report']['artifacts']['markdown'], str(markdown_path.resolve()))
            self.assertEqual(payload['report']['artifacts']['html'], str(html_path.resolve()))
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())


if __name__ == '__main__':
    unittest.main()
