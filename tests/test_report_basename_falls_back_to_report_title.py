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


class ReportBasenameFallsBackToReportTitleTests(unittest.TestCase):
    def test_report_dir_uses_report_title_slug_when_basename_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            report_dir = tmp / 'reports'
            scenario_path.write_text(
                'proposal: Ship staged delegate education updates.
'
                'stakeholders:
'
                '  - name: Delegates
'
                '    stance: cautious
'
                'report_title: Delegate Education Review
',
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path), '--report-dir', str(report_dir)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload['report']['artifacts']['basename'], 'delegate-education-review')
            self.assertTrue((report_dir / 'delegate-education-review.json').exists())
            self.assertTrue((report_dir / 'delegate-education-review.md').exists())
            self.assertTrue((report_dir / 'delegate-education-review.html').exists())


if __name__ == '__main__':
    unittest.main()
