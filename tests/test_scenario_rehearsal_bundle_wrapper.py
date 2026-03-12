from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ScenarioRehearsalBundleWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_rehearsal_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_path = tmp_path / "scenario.json"
            scenario_path.write_text(json.dumps({
                "scenario_rehearsal_bundle": {
                    "proposal": "Ship a staged treasury alert policy before the next payout window.",
                    "stakeholders": ["delegates"],
                    "report": {"title": "Scenario rehearsal bundle demo"}
                }
            }), encoding="utf-8")

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
                env={**__import__("os").environ, "PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["proposal"], "Ship a staged treasury alert policy before the next payout window.")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario rehearsal bundle demo")


if __name__ == "__main__":
    unittest.main()
