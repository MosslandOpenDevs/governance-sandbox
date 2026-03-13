from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportBundleTagAliasTests(unittest.TestCase):
    def test_report_bundle_tag_drives_generated_report_basenames(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            report_dir = tmp / "reports"
            scenario_path.write_text(json.dumps({
                "proposal": "Pilot delegate office hours before the next vote.",
                "stakeholders": ["delegates", "community"],
                "report_bundle_tag": "delegate-office-hours"
            }), encoding="utf-8")

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
                env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue((report_dir / "delegate-office-hours.json").exists())
            self.assertTrue((report_dir / "delegate-office-hours.md").exists())
            self.assertTrue((report_dir / "delegate-office-hours.html").exists())
            self.assertIn('"basename": "delegate-office-hours"', completed.stdout)


if __name__ == "__main__":
    unittest.main()
