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


class ReportOutputKeyAliasTests(unittest.TestCase):
    def test_run_supports_report_output_key_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.json'
            scenario_path.write_text(
                json.dumps(
                    {
                        'proposal': 'Ship a delegate-ready governance memo.',
                        'stakeholders': [{'name': 'Delegate circle', 'preset': 'delegates'}],
                        'report_output_key': 'delegate-memo-key',
                    }
                ),
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload['report']['artifacts']['basename'], 'delegate-memo-key')

    def test_run_supports_report_outputs_output_key_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            scenario_path.write_text(
                """proposal: |
  Publish a staged treasury status note.
stakeholders:
  - name: Community delegates
    preset: delegates
report:
  outputs:
    output_key: treasury-status-key
""",
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload['report']['artifacts']['basename'], 'treasury-status-key')


if __name__ == '__main__':
    unittest.main()
