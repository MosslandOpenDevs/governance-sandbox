from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ScenarioTopLevelWrapperTest(unittest.TestCase):
    def test_run_accepts_top_level_scenario_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario": {
                            "proposal": "Ship a treasury review workflow with reversible guardrails.",
                            "stakeholders": [
                                {"name": "Delegate council", "preset": "delegates"},
                                {"name": "Core contributors", "preset": "contributors"},
                            ],
                            "report": {
                                "title": "Wrapped scenario memo",
                                "summary": "Plain scenario wrapper proving scenario file import plus report metadata handoff.",
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
            self.assertEqual(payload["proposal"], "Ship a treasury review workflow with reversible guardrails.")
            self.assertEqual(payload["scenario"]["report_title"], "Wrapped scenario memo")
            self.assertEqual(
                payload["scenario"]["report_summary"],
                "Plain scenario wrapper proving scenario file import plus report metadata handoff.",
            )
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
