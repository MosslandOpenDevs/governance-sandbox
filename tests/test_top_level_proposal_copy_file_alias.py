from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TopLevelProposalCopyFileAliasTests(unittest.TestCase):
    def test_run_accepts_top_level_proposal_copy_file_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal_file = tmp / 'proposal.md'
            proposal_file.write_text('Ship a grants council with quarterly accountability reviews.', encoding='utf-8')
            scenario_file = tmp / 'scenario.yaml'
            scenario_file.write_text(
                '\n'.join([
                    'proposal_copy_file: proposal.md',
                    'stakeholders:',
                    '  - delegates',
                    '  - community',
                    'report:',
                    '  title: Grants council memo',
                ]),
                encoding='utf-8',
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    str(scenario_file),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload['proposal'], 'Ship a grants council with quarterly accountability reviews.')
            self.assertEqual([response['preset'] for response in payload['responses']], ['delegates', 'community'])


if __name__ == '__main__':
    unittest.main()
