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


class ReportWatchersAliasTests(unittest.TestCase):
    def test_run_supports_report_watchers_aliases_in_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            markdown_path = tmp / 'report.md'
            html_path = tmp / 'report.html'
            scenario_path.write_text(
                '''proposal: Publish one delegate-ready treasury checkpoint before the next vote.
stakeholders:
  - name: Delegate circle
    preset: delegates
report:
  watchers:
    - forum ops
    - treasury stewards
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
            self.assertEqual(payload['scenario']['report_audience'], 'forum ops, treasury stewards')
            self.assertIn('## Report audience\nforum ops, treasury stewards', markdown_path.read_text(encoding='utf-8'))
            self.assertIn('<strong>Report audience:</strong> forum ops, treasury stewards', html_path.read_text(encoding='utf-8'))

    def test_readme_mentions_watchers_alias_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_REPORT_WATCHERS_ALIAS_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_REPORT_WATCHERS_ALIAS_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
