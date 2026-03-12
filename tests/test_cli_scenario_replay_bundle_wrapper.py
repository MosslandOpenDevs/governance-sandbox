from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class CliScenarioReplayBundleWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_replay_bundle_wrapper(self) -> None:
        scenario = {
            'scenario_replay_bundle': {
                'proposal': 'Adopt a staged treasury reporting cadence with monthly snapshots.',
                'stakeholders': [
                    {'name': 'Delegate Council', 'preset': 'delegates'},
                    {'name': 'Core Contributors', 'preset': 'contributors'},
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'scenario.json'
            path.write_text(json.dumps(scenario), encoding='utf-8')

            completed = subprocess.run(
                [
                    'python3',
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    str(path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                check=True,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload['scenario']['scenario_file'], str(path.resolve()))
        self.assertEqual(payload['summary']['stakeholder_count'], 2)


if __name__ == '__main__':
    unittest.main()
