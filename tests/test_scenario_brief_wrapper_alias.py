from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


class ScenarioBriefWrapperAliasTest(unittest.TestCase):
    def test_run_accepts_top_level_scenario_brief_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.json'
            scenario_path.write_text(
                json.dumps(
                    {
                        'scenario_brief': {
                            'proposal': 'Pilot a contributor budget review with delegate observers and monthly reporting.',
                            'stakeholders': [
                                {'name': 'DAO ops', 'preset': 'dao'},
                                {'name': 'Delegates', 'preset': 'delegates'},
                            ],
                            'report': {
                                'title': 'Scenario brief wrapper memo',
                                'summary': 'Scenario brief wrapper should load proposal and stakeholder inputs without reshaping the file.',
                            },
                        }
                    }
                ),
                encoding='utf-8',
            )

            completed = subprocess.run(
                [
                    'python3',
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload['scenario']['report_title'], 'Scenario brief wrapper memo')
            self.assertEqual(len(payload['responses']), 2)


if __name__ == '__main__':
    unittest.main()
