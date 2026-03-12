import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class ScenarioDossierWrapperTests(unittest.TestCase):
    def test_scenario_dossier_wrapper_loads_proposal_and_stakeholders(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        payload = {
            'scenario_dossier': {
                'proposal': {'title': 'Treasury guardrails', 'summary': 'Ship monthly disclosure pack.'},
                'stakeholders': [
                    {'name': 'Delegate council', 'preset': 'delegates'},
                    {'name': 'Core contributors', 'preset': 'contributors'},
                ],
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.json'
            scenario_path.write_text(json.dumps(payload), encoding='utf-8')
            completed = subprocess.run(
                ['python3', '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)],
                cwd=repo_root,
                env={'PYTHONPATH': str(repo_root / 'src')},
                text=True,
                capture_output=True,
                check=True,
            )
        output = json.loads(completed.stdout)
        self.assertIn('Treasury guardrails', output['proposal'])
        self.assertEqual(len(output['responses']), 2)
        self.assertEqual(output['responses'][0]['preset'], 'delegates')


if __name__ == '__main__':
    unittest.main()
