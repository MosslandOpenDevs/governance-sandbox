from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, '-m', 'governance_sandbox.cli', 'run']


class ScenarioFileProposalOutlineAliasTests(unittest.TestCase):
    def test_scenario_file_accepts_proposal_outline_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.json'
            scenario_path.write_text(
                json.dumps(
                    {
                        'proposal_outline': {
                            'title': 'Treasury stewardship update',
                            'summary': 'Move the working group proposal through a gated pilot.',
                            'sections': [
                                {
                                    'title': 'Pilot guardrails',
                                    'body': 'Cap spending and publish a monthly rollback review.',
                                }
                            ],
                        },
                        'stakeholders': ['dao', 'delegates'],
                    }
                ),
                encoding='utf-8',
            )

            completed = subprocess.run(
                [*CLI, '--scenario-file', str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertIn('Treasury stewardship update', payload['proposal'])
            self.assertIn('Pilot guardrails', payload['proposal'])
            self.assertEqual(payload['summary']['stakeholder_count'], 2)


if __name__ == '__main__':
    unittest.main()
