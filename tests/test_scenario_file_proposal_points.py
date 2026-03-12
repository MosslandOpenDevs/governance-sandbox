from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioFileProposalPointsTests(unittest.TestCase):
    def test_run_supports_proposal_points_from_scenario_file(self) -> None:
        scenario_text = textwrap.dedent(
            """
            proposal:
              title: Treasury runway reset
              summary: Reallocate 12% of the treasury to contributor retention.
              points:
                - Keep the grants runway above 18 months.
                - Publish a monthly retention dashboard.
            stakeholders:
              - name: Core contributors
                preset: contributors
              - name: Delegates
                preset: delegates
            """
        ).strip()
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_file = Path(tmpdir) / 'scenario.yaml'
            report_dir = Path(tmpdir) / 'artifacts'
            scenario_file.write_text(scenario_text, encoding='utf-8')

            completed = subprocess.run(
                [
                    'python3', '-m', 'governance_sandbox.cli', 'run',
                    '--scenario-file', str(scenario_file),
                    '--report-dir', str(report_dir),
                ],
                cwd=ROOT,
                env={'PYTHONPATH': 'src'},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertIn('Key points:', payload['proposal'])
            self.assertIn('- Keep the grants runway above 18 months.', payload['proposal'])
            self.assertIn('- Publish a monthly retention dashboard.', payload['proposal'])
            markdown_report = Path(payload['report']['artifacts']['markdown']).read_text(encoding='utf-8')
            self.assertIn('Key points:', markdown_report)
            self.assertIn('- Keep the grants runway above 18 months.', markdown_report)


if __name__ == '__main__':
    unittest.main()
