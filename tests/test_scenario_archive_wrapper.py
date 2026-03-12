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


class ScenarioArchiveWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_archive_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario_archive:
  proposal: Stage a treasury guardrail update before the next delegate vote.
  stakeholders:
    - dao
  report:
    title: Scenario archive wrapper demo
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
            self.assertEqual(payload["proposal"], "Stage a treasury guardrail update before the next delegate vote.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario archive wrapper demo")
            self.assertEqual(payload["responses"][0]["preset"], "dao")


if __name__ == "__main__":
    unittest.main()
