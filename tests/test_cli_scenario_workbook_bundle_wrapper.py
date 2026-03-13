from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliScenarioWorkbookBundleWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_workbook_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            scenario_path = tmp_path / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_workbook_bundle": {
                            "proposal": "Stage treasury unlocks behind milestone sign-off.",
                            "stakeholders": [
                                {"name": "DAO delegates", "preset": "delegates"},
                                {"name": "Community builders", "preset": "contributors"},
                            ],
                            "report": {
                                "title": "Milestone sign-off memo",
                                "outputs": {"basename": "milestone-sign-off"},
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            report_dir = tmp_path / "reports"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Stage treasury unlocks behind milestone sign-off.")
            self.assertTrue(payload["report"]["artifacts"]["markdown"].endswith("milestone-sign-off.md"))


if __name__ == "__main__":
    unittest.main()
