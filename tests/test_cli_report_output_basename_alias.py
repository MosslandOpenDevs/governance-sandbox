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


class ReportOutputBasenameAliasTest(unittest.TestCase):
    def test_top_level_report_output_basename_drives_report_bundle(self) -> None:
        scenario = {
            "proposal": "Ship a delegate onboarding sprint with capped reviewer budget.",
            "stakeholders": {"Treasury Council": "dao", "Delegate Desk": "delegates"},
            "report_output_basename": "delegate-onboarding-bundle",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            report_dir = tmp / "reports"
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-onboarding-bundle")
            self.assertTrue((report_dir / "delegate-onboarding-bundle.json").exists())
            self.assertTrue((report_dir / "delegate-onboarding-bundle.md").exists())
            self.assertTrue((report_dir / "delegate-onboarding-bundle.html").exists())


if __name__ == "__main__":
    unittest.main()
