from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ScenarioPlaygroundWrapperAliasTest(unittest.TestCase):
    def test_scenario_playground_wrapper_loads_nested_scenario(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario-playground.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_playground": {
                            "proposal": "Ship a staged treasury dashboard rollout.",
                            "stakeholders": [
                                {"name": "Delegate Council", "preset": "delegates"},
                                {"name": "Core Contributors", "preset": "contributors"},
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["proposal"], "Ship a staged treasury dashboard rollout.")
        self.assertEqual(len(payload["responses"]), 2)
        self.assertEqual(payload["responses"][0]["preset"], "delegates")
        self.assertEqual(payload["responses"][1]["preset"], "contributors")


if __name__ == "__main__":
    unittest.main()
