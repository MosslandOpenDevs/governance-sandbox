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


class ScenarioSourceInputsAliasTests(unittest.TestCase):
    def test_run_uses_top_level_inputs_source_alias(self) -> None:
        scenario = {
            "inputs": {
                "proposal": "Ship scenario import reports.",
                "stakeholders": ["DAO", "Community"],
                "source": "fixtures/demo-scenario.yaml",
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONPATH": str(SRC)},
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["scenario"]["scenario_file"], str(scenario_path.resolve()))
        self.assertEqual(payload["report"]["scenario_file"], str(scenario_path.resolve()))

    def test_run_uses_stdin_inputs_source_alias(self) -> None:
        scenario = {
            "inputs": {
                "proposal": "Ship scenario import reports.",
                "stakeholders": ["DAO", "Community"],
                "source": "fixtures/stdin-scenario.yaml",
            }
        }

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "governance_sandbox.cli",
                "run",
                "--scenario-file",
                "-",
            ],
            cwd=ROOT,
            input=json.dumps(scenario),
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(SRC)},
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["scenario"]["scenario_file"], "fixtures/stdin-scenario.yaml")
        self.assertEqual(payload["report"]["scenario_file"], "fixtures/stdin-scenario.yaml")


if __name__ == "__main__":
    unittest.main()
