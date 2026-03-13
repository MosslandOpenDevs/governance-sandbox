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


class ReportBundleCodeAliasTests(unittest.TestCase):
    def test_report_bundle_code_alias_sets_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario = tmp / 'scenario.yaml'
            report_dir = tmp / 'reports'
            scenario.write_text(
                'proposal: Ship a treasury dashboard\nstakeholders:\n  - name: Delegates\n    stance: supportive\nreport_bundle_code: treasury-dashboard-code\n',
                encoding='utf-8',
            )

            completed = subprocess.run(
                [
                    sys.executable, '-m', 'governance_sandbox.cli', 'run',
                    '--scenario-file', str(scenario),
                    '--report-dir', str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            self.assertTrue((report_dir / 'treasury-dashboard-code.json').exists())
            self.assertTrue((report_dir / 'treasury-dashboard-code.md').exists())
            self.assertTrue((report_dir / 'treasury-dashboard-code.html').exists())
            self.assertEqual(payload['report']['artifacts']['basename'], 'treasury-dashboard-code')


if __name__ == '__main__':
    unittest.main()
