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


class GovernanceSandboxScenarioRelativeReportDirTests(unittest.TestCase):
    def test_scenario_relative_report_dir_resolves_from_scenario_file_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_dir = tmp / "fixtures"
            scenario_dir.mkdir()
            scenario_path = scenario_dir / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Ship staged treasury messaging update.",
                        "stakeholders": [
                            {"name": "Delegate council", "preset": "delegates"},
                            {"name": "Community stewards", "preset": "community"},
                        ],
                        "report": {
                            "outputs": {
                                "report_dir": "artifacts/bundle",
                                "bundle_name": "relative-report-dir"
                            }
                        }
                    }
                ),
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
            report_dir = scenario_dir / "artifacts" / "bundle"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "relative-report-dir.json").exists())
            self.assertTrue((report_dir / "relative-report-dir.md").exists())
            self.assertTrue((report_dir / "relative-report-dir.html").exists())


if __name__ == "__main__":
    unittest.main()
