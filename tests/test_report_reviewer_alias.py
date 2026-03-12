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


class ReportReviewerAliasTests(unittest.TestCase):
    def test_run_supports_singular_report_reviewer_aliases_in_markdown_and_html(self) -> None:
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
  title: Singular reviewer alias replay
  reviewer: Delegate forum lead
''',
                encoding='utf-8',
            )

            completed = subprocess.run(
                [
                    sys.executable, '-m', 'governance_sandbox.cli', 'run',
                    '--scenario-file', str(scenario_path),
                    '--report-markdown', str(markdown_path),
                    '--report-html', str(html_path),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload['scenario']['report_audience'], 'Delegate forum lead')
            self.assertIn('## Report audience\nDelegate forum lead', markdown_path.read_text(encoding='utf-8'))
            self.assertIn('<strong>Report audience:</strong> Delegate forum lead', html_path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
