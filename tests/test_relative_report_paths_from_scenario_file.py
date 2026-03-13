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


class RelativeReportPathsFromScenarioFileTests(unittest.TestCase):
    def test_run_resolves_relative_report_paths_from_scenario_file_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            scenario_dir = workspace / "fixtures"
            scenario_dir.mkdir()
            scenario_path = scenario_dir / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Ship a scoped governance memo.",
                        "stakeholders": [{"name": "Delegate council", "preset": "delegates"}],
                        "report": {
                            "outputs": {
                                "json": "reports/demo/report.json",
                                "markdown": "reports/demo/report.md",
                                "html": "reports/demo/report.html"
                            }
                        }
                    }
                ),
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
            report_dir = scenario_dir / "reports" / "demo"
            self.assertEqual(payload["report"]["artifacts"]["directory"], None)
            self.assertEqual(payload["report"]["artifacts"]["json"], str((report_dir / "report.json").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str((report_dir / "report.md").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["html"], str((report_dir / "report.html").resolve()))
            self.assertTrue((report_dir / "report.json").exists())
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
