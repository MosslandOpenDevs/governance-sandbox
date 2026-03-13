from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioStagePackWrapperTests(unittest.TestCase):
    def test_stage_pack_wrapper_loads_scenario_file_and_reports(self) -> None:
        scenario = {
            "scenario_stage_pack": {
                "proposal": "Adopt staged delegate scorecards before treasury votes.",
                "stakeholders": [
                    {"name": "DAO Council", "preset": "dao"},
                    {"name": "Lead Delegates", "preset": "delegates"},
                ],
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "stage-pack.json"
            report_dir = Path(tmpdir) / "reports"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")

            completed = subprocess.run(
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
                capture_output=True,
                text=True,
                check=True,
                env={"PYTHONPATH": str(ROOT / "src")},
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["proposal"], "Adopt staged delegate scorecards before treasury votes.")
            self.assertEqual(len(payload["responses"]), 2)
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
