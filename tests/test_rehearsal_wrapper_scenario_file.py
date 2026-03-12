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


class RehearsalWrapperScenarioFileTests(unittest.TestCase):
    def test_rehearsal_wrapper_fixture_drives_markdown_report_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / 'bundle'
            scenario_path = ROOT / 'examples' / 'scenario-rehearsal-wrapper.yaml'

            result = subprocess.run(
                [
                    sys.executable,
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    str(scenario_path),
                    '--report-dir',
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload['scenario']['name'], 'Rehearsal wrapper import')
            self.assertEqual(payload['scenario']['report_title'], 'Rehearsal wrapper memo')
            self.assertEqual(payload['report']['artifacts']['basename'], 'rehearsal-wrapper')
            markdown_report = (report_dir / 'rehearsal-wrapper.md').read_text(encoding='utf-8')
            self.assertIn('## Scenario\nRehearsal wrapper import', markdown_report)
            self.assertIn('## Report title\nRehearsal wrapper memo', markdown_report)


if __name__ == '__main__':
    unittest.main()
