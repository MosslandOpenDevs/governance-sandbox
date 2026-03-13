from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliScenarioReportBundleWrapperTests(unittest.TestCase):
    def test_scenario_report_bundle_wrapper_loads_nested_payload(self) -> None:
        payload = {
            "scenario_report_bundle": {
                "proposal": "Ship a treasury dashboard",
                "stakeholders": [{"name": "Delegates", "stance": "supportive"}],
                "report_bundle_code": "treasury-dashboard-wrapper"
            }
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            scenario_path = Path(tmp_dir) / "scenario.json"
            report_dir = Path(tmp_dir) / "artifacts"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")

            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(PYTHONPATH=str(ROOT / "src"))},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn("treasury-dashboard-wrapper", completed.stdout)
            self.assertTrue((report_dir / "treasury-dashboard-wrapper.md").exists())
            self.assertTrue((report_dir / "treasury-dashboard-wrapper.html").exists())
            self.assertTrue((report_dir / "treasury-dashboard-wrapper.json").exists())


if __name__ == "__main__":
    unittest.main()
