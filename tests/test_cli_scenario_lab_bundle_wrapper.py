from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class CliScenarioLabBundleWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_lab_bundle_wrapper(self) -> None:
        scenario = {
            'scenario_lab_bundle': {
                'proposal': 'Stage grant milestone reviews with monthly DAO checkpoints.',
                'stakeholders': [
                    {'name': 'Delegate Circle', 'preset': 'delegates'},
                    {'name': 'Community Stewards', 'preset': 'community'},
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
