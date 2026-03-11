from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


class ReportOutputFolderAliasTests(unittest.TestCase):
    def test_run_supports_report_output_folder_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            scenario_path.write_text(textwrap.dedent('''\
                proposal: Add a staged delegate review.
                stakeholders:
                  - Delegates
                  - Community
                report_output_folder: exports/reports
                report_name: Delegate Review Packet
                '''), encoding='utf-8')

            result = subprocess.run(
                [
                    sys.executable, '-m', 'governance_sandbox.cli', 'run',
                    '--scenario-file', str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            report_dir = scenario_path.parent / 'exports' / 'reports'
            self.assertEqual(payload['report']['artifacts']['directory'], str(report_dir.resolve()))
            self.assertTrue((report_dir / 'delegate-review-packet.json').exists())
            self.assertTrue((report_dir / 'delegate-review-packet.md').exists())
            self.assertTrue((report_dir / 'delegate-review-packet.html').exists())


if __name__ == '__main__':
    unittest.main()
