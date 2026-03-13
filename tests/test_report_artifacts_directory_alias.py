import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class ReportArtifactsDirectoryAliasTests(unittest.TestCase):
    def test_scenario_file_supports_artifacts_directory_alias_for_report_bundle(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        payload = {
            "proposal": {
                "title": "Treasury disclosure cadence",
                "summary": "Publish a monthly governance memo with KPI deltas.",
            },
            "stakeholders": [
                {"name": "Delegate council", "preset": "delegates"},
                {"name": "Community stewards", "preset": "community"},
            ],
            "report": {
                "title": "Disclosure memo",
                "outputs": {
                    "basename": "disclosure-memo",
                    "artifacts_directory": "artifacts/reports"
                }
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
            self.assertTrue(output['report']['artifacts']['markdown'].endswith('artifacts/reports/disclosure-memo.md'))
            self.assertTrue(output['report']['artifacts']['html'].endswith('artifacts/reports/disclosure-memo.html'))
            self.assertTrue(output['report']['artifacts']['json'].endswith('artifacts/reports/disclosure-memo.json'))
