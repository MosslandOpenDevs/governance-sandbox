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


class ScenarioRecordWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_record_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario_record:\n  proposal: Publish a staged treasury checkpoint before the next vote.\n  stakeholders:\n    - delegates\n  report:\n    title: Scenario record wrapper demo\n""",
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
            self.assertEqual(payload["proposal"], "Publish a staged treasury checkpoint before the next vote.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario record wrapper demo")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")


if __name__ == "__main__":
    unittest.main()
