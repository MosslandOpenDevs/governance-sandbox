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


class ScenarioSheetWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_sheet_wrapper_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario-sheet.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_sheet": {
                            "scenario": {
                                "name": "Scenario sheet rehearsal",
                                "context": "Replay a proposal packet from a single wrapped fixture.",
                            },
                            "proposal": "Add checkpoint-based treasury vote rehearsal before execution.",
                            "stakeholders": [
                                {"name": "Delegate circle", "preset": "delegates"},
                                {"name": "Builder pod", "preset": "contributors"},
                            ],
                            "report": {"title": "Scenario sheet memo"},
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
            self.assertEqual(payload["scenario"]["name"], "Scenario sheet rehearsal")
            self.assertEqual(payload["scenario"]["context"], "Replay a proposal packet from a single wrapped fixture.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario sheet memo")
            self.assertEqual([item["preset"] for item in payload["responses"]], ["delegates", "contributors"])


if __name__ == "__main__":
    unittest.main()
