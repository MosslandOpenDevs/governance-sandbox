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


class NestedScenarioInputsTests(unittest.TestCase):
    def test_run_accepts_nested_scenario_inputs_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                """scenario:
  name: Nested DAO rehearsal
  inputs:
    proposal: Add a staged delegate budget with rollback checkpoints.
    stakeholder_map:
      Delegate council: delegates
      Builder guild: contributors
report:
  title: Nested DAO rehearsal memo
""",
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
            self.assertEqual(payload["scenario"]["name"], "Nested DAO rehearsal")
            self.assertEqual(payload["proposal"], "Add a staged delegate budget with rollback checkpoints.")
            self.assertEqual(len(payload["responses"]), 2)
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "contributors")


if __name__ == "__main__":
    unittest.main()
