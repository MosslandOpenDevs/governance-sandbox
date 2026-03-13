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


class ReportOutputsLabelAliasTests(unittest.TestCase):
    def test_run_supports_report_outputs_label_alias(self) -> None:
        scenario = '''
proposal:
  title: Delegate review
  summary: Scenario fixture for report.outputs.label alias.
stakeholders:
  - name: Delegates
    stance: support
    influence: 0.7
report:
  outputs:
    label: delegate-review-card
'''
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.yaml'
            scenario_path.write_text(scenario, encoding='utf-8')
            out_dir = Path(tmpdir) / 'artifacts'
            result = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path), '--report-dir', str(out_dir)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload['scenario']['report_basename'], 'delegate-review-card')
            self.assertTrue(payload['report']['artifacts']['json'].endswith('delegate-review-card.json'))


if __name__ == '__main__':
    unittest.main()
