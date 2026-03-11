from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ScenarioConfigWrapperAliasTest(unittest.TestCase):
    def test_run_accepts_top_level_scenario_config_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_config": {
                            "proposal": "Adopt staged delegate incentives with a transparent review window.",
                            "stakeholders": [
                                {"name": "DAO delegates", "preset": "delegates"},
                                {"name": "Community stewards", "preset": "community"},
                            ],
                            "report": {
                                "title": "Scenario config memo",
                                "summary": "Wrapper alias proving scenario_config imports proposal, presets, and report metadata.",
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
            self.assertEqual(payload["proposal"], "Adopt staged delegate incentives with a transparent review window.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario config memo")
            self.assertEqual(
                payload["scenario"]["report_summary"],
                "Wrapper alias proving scenario_config imports proposal, presets, and report metadata.",
            )
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
