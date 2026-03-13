import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


class ScenarioSourceFileAliasTests(unittest.TestCase):
    def test_run_supports_scenario_source_file_alias(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                textwrap.dedent(
                    """\
                    proposal: Expand the delegate briefing cadence to every two weeks.
                    stakeholders:
                      - dao
                      - delegates
                      - community
                    scenario_source_file: fixtures/rehearsal-source.yaml
                    report:
                      title: Scenario source file alias
                      outputs:
                        basename: scenario-source-file-alias
                    """
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["scenario"]["scenario_file"], "fixtures/rehearsal-source.yaml")
            self.assertEqual(payload["scenario"]["scenario_format"], "yaml")
            self.assertEqual(payload["report"]["scenario_file"], "fixtures/rehearsal-source.yaml")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "scenario-source-file-alias")


if __name__ == "__main__":
    unittest.main()
