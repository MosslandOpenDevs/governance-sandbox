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


class ScenarioPlaybookWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_playbook_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario_playbook:
  proposal: Ship the scenario-file import before the next delegate review.
  stakeholders:
    - dao
  report:
    title: Scenario playbook wrapper demo
""",
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
            self.assertEqual(payload["proposal"], "Ship the scenario-file import before the next delegate review.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario playbook wrapper demo")
            self.assertEqual(payload["responses"][0]["preset"], "dao")


if __name__ == "__main__":
    unittest.main()
