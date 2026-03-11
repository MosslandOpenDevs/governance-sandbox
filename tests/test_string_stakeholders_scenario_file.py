from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "governance_sandbox.cli", "run"]


class StringStakeholdersScenarioFileTests(unittest.TestCase):
    def test_scenario_file_accepts_comma_separated_stakeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Ship a staged treasury automation pilot.",
                        "stakeholders": "dao, delegates, community",
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [*CLI, "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual([response["name"] for response in payload["responses"]], ["dao", "delegates", "community"])
            self.assertEqual(payload["summary"]["stakeholder_count"], 3)


if __name__ == "__main__":
    unittest.main()
