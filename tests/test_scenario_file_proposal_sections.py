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


class ScenarioFileProposalSectionsTests(unittest.TestCase):
    def test_scenario_file_supports_structured_proposal_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.json'
            scenario_path.write_text(
                json.dumps({
                    'proposal': {
                        'title': 'Treasury automation rollout',
                        'summary': 'Ship the rollout in two visible stages.',
                        'sections': [
                            {
                                'title': 'Stage 1',
                                'body': 'Ship treasury alerts first.',
                                'points': ['keep manual signoff', 'publish weekly metrics'],
                            },
                            {
                                'title': 'Stage 2',
                                'body': 'Expand to recurring execution after review.',
                            },
                        ],
                    },
                    'stakeholders': [
                        {'name': 'Delegate council', 'preset': 'delegates'},
                        {'name': 'Core builders', 'preset': 'contributors'},
                    ],
                }),
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertIn('Treasury automation rollout', payload['proposal'])
            self.assertIn('Sections:', payload['proposal'])
            self.assertIn('Stage 1', payload['proposal'])
            self.assertIn('keep manual signoff', payload['proposal'])
            self.assertIn('Stage 2', payload['proposal'])


if __name__ == '__main__':
    unittest.main()
