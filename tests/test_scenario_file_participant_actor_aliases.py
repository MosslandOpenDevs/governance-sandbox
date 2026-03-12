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


class ScenarioFileParticipantActorAliasesTests(unittest.TestCase):
    def test_run_supports_participant_and_actor_name_aliases_in_scenario_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Publish a treasury checkpoint memo before the vote.",
                        "stakeholders": [
                            {"participant": "Delegate council", "preset": "delegates"},
                            {"actor": "Builder guild", "preset": "contributors"},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["responses"][0]["name"], "Delegate council")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["name"], "Builder guild")
            self.assertEqual(payload["responses"][1]["preset"], "contributors")


if __name__ == "__main__":
    unittest.main()
