from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TraitInputAliasTests(unittest.TestCase):
    def test_run_accepts_trait_alias_maps_from_scenario_file(self) -> None:
        scenario = {
            "proposal": "Launch a delegate tooling retro.",
            "traits": {
                "DAO Council": "dao",
                "Active Delegates": "delegates",
            },
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")

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
                env={"PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual([item["preset"] for item in payload["responses"]], ["dao", "delegates"])


if __name__ == "__main__":
    unittest.main()
