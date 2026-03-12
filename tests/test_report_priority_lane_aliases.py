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


class ReportPriorityLaneAliasesTests(unittest.TestCase):
    def test_run_supports_priority_lane_aliases_in_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            markdown_path = tmp / 'report.md'
            html_path = tmp / 'report.html'
            scenario_path.write_text(
                '''proposal: Ship a staged treasury automation rollout with emergency pause controls.
stakeholders:
  - name: DAO delegates
    preset: delegates
  - name: Core contributors
    preset: contributors
report:
  title: Priority lane alias replay
  priority_lane: Immediate follow-up before forum post
''',
                encoding='utf-8',
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    str(scenario_path),
                    '--report-markdown',
                    str(markdown_path),
                    '--report-html',
                    str(html_path),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            markdown = markdown_path.read_text(encoding='utf-8')
            html = html_path.read_text(encoding='utf-8')

            self.assertEqual(payload['scenario']['report_priority'], 'Immediate follow-up before forum post')
            self.assertIn('## Report priority\nImmediate follow-up before forum post', markdown)
            self.assertIn('<strong>Report priority:</strong> Immediate follow-up before forum post', html)


if __name__ == '__main__':
    unittest.main()
