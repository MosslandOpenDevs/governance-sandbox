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


class ReportReviewTeamAliasTests(unittest.TestCase):
    def test_run_supports_nested_report_review_team_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            markdown_path = tmp / 'report.md'
            html_path = tmp / 'report.html'
            scenario_path.write_text(
                '''proposal: Add a treasury guardrail review before the vote.
stakeholders:
  - delegates
report:
  review_team:
    - forum reviewers
    - treasury stewards
''',
                encoding='utf-8',
            )

            result = subprocess.run(
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

            payload = json.loads(result.stdout)
            self.assertEqual(payload['scenario']['report_audience'], 'forum reviewers, treasury stewards')
            self.assertIn('## Report audience\nforum reviewers, treasury stewards', markdown_path.read_text(encoding='utf-8'))
            self.assertIn('<strong>Report audience:</strong> forum reviewers, treasury stewards', html_path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
