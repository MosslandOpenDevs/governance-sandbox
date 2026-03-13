from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProposalCopyFileAliasTests(unittest.TestCase):
    def test_proposal_copy_file_loads_markdown_body_and_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal_path = tmp / 'proposal.md'
            proposal_path.write_text('# Treasury update\n\nShip a staged contributor budget review.', encoding='utf-8')
            scenario_path = tmp / 'scenario.json'
            report_dir = tmp / 'reports'
            scenario_path.write_text(json.dumps({
                'proposal_copy_file': 'proposal.md',
                'stakeholders': ['dao', 'delegates'],
            }), encoding='utf-8')

            completed = subprocess.run(
                [
                    sys.executable, '-m', 'governance_sandbox.cli', 'run',
                    '--scenario-file', str(scenario_path),
                    '--report-dir', str(report_dir),
                ],
                cwd=ROOT, capture_output=True, text=True, check=True, env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
            )

            payload = json.loads(completed.stdout)
            self.assertIn('Ship a staged contributor budget review.', payload['proposal'])
            self.assertTrue((report_dir / 'report.md').exists())
            self.assertTrue((report_dir / 'report.html').exists())


if __name__ == '__main__':
    unittest.main()
