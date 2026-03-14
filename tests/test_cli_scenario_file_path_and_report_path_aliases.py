from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioFilePathAndReportPathAliasTests(unittest.TestCase):
    def test_cli_accepts_scenario_file_path_and_report_path_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            json_path = tmp / "report.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Adopt a staged grants budget with monthly reporting.",
                        "stakeholders": ["DAO delegates", "Contributors", "Community reviewers"],
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
                    "--scenario-file-path",
                    str(scenario_path),
                    "--report-markdown-path",
                    str(markdown_path),
                    "--report-html-path",
                    str(html_path),
                    "--report-json-path",
                    str(json_path),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(result.stdout)
            self.assertIn("responses", payload)
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertTrue(json_path.exists())


if __name__ == "__main__":
    unittest.main()
