import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


class ProposalInputMarkdownPathAliasTest(unittest.TestCase):
    def test_run_accepts_proposal_input_markdown_path_alias(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal_path = tmp / 'proposal.md'
            scenario_path = tmp / 'scenario.yaml'
            report_json = tmp / 'report.json'
            report_md = tmp / 'report.md'
            report_html = tmp / 'report.html'

            proposal_path.write_text('# Upgrade treasury policy\n\nShip a markdown-backed scenario input.', encoding='utf-8')
            scenario_path.write_text(textwrap.dedent('''\
                proposal_input_markdown_path: proposal.md
                stakeholders:
                  - Alice
                  - Bob
                report:
                  outputs:
                    basename: markdown-path-demo
                '''), encoding='utf-8')

            completed = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path), '--report-json', str(report_json), '--report-markdown', str(report_md), '--report-html', str(report_html)],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
                env={'PYTHONPATH': str(repo_root / 'src')},
            )

            payload = json.loads(report_json.read_text(encoding='utf-8'))
            self.assertIn('markdown-backed scenario input', payload['proposal'])
            self.assertEqual(payload['report']['artifacts']['basename'], 'markdown-path-demo')
            self.assertTrue(report_md.exists())
            self.assertTrue(report_html.exists())
            self.assertIn('recommendation', completed.stdout)


if __name__ == '__main__':
    unittest.main()
