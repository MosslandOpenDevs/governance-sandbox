from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ScenarioStageWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_stage_wrapper_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario-stage.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_stage": {
                            "scenario": {
                                "name": "Scenario stage rehearsal",
                                "context": "Load a staged governance rehearsal from one wrapped file.",
                            },
                            "proposal": "Ship JSON/YAML scenario imports with markdown and HTML memo artifacts.",
                            "stakeholders": [
                                {"name": "Delegate pod", "preset": "delegates"},
                                {"name": "Community circle", "preset": "community"},
                            ],
                            "report": {"title": "Scenario stage memo"},
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Scenario stage rehearsal")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario stage memo")
            self.assertEqual([item["preset"] for item in payload["responses"]], ["delegates", "community"])


if __name__ == "__main__":
    unittest.main()
