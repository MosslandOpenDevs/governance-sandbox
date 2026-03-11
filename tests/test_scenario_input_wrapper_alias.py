from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ScenarioInputWrapperAliasTest(unittest.TestCase):
    def test_run_accepts_top_level_scenario_input_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_input": {
                            "proposal": "Adopt a staged grants committee rollout with delegate review.",
                            "stakeholders": [
                                {"name": "Delegate council", "preset": "delegates"},
                                {"name": "Community stewards", "preset": "community"},
                            ],
                            "report": {
                                "title": "Scenario input wrapper memo",
                                "summary": "Wrapper alias keeps one imported scenario tied to a generated memo.",
                            },
                        }
                    }
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
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["proposal"], "Adopt a staged grants committee rollout with delegate review.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario input wrapper memo")
            self.assertEqual(payload["scenario"]["report_summary"], "Wrapper alias keeps one imported scenario tied to a generated memo.")
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
