from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class GovernanceSandboxCliTests(unittest.TestCase):
    def test_run_supports_json_scenario_file_and_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            json_path = tmp / "report.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "name": "Treasury reallocation dry run",
                        "context": "Emergency budget review before the next DAO vote.",
                        "proposal": "Shift part of the treasury budget to community growth experiments.",
                        "stakeholders": [
                            {"name": "DAO council", "preset": "dao"},
                            {"name": "Delegate cohort", "preset": "delegates"},
                        ],
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
                    "--report-markdown",
                    str(markdown_path),
                    "--report-html",
                    str(html_path),
                    "--report-json",
                    str(json_path),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Shift part of the treasury budget to community growth experiments.")
            self.assertEqual(payload["scenario"]["name"], "Treasury reallocation dry run")
            self.assertEqual(payload["scenario"]["context"], "Emergency budget review before the next DAO vote.")
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertTrue(json_path.exists())
            markdown_report = markdown_path.read_text(encoding="utf-8")
            html_report = html_path.read_text(encoding="utf-8")
            self.assertIn("# Governance Sandbox Report", markdown_report)
            self.assertIn("## Scenario\nTreasury reallocation dry run", markdown_report)
            self.assertIn("## Context\nEmergency budget review before the next DAO vote.", markdown_report)
            self.assertIn("### DAO council (dao)", markdown_report)
            self.assertIn("<title>Governance Sandbox Report</title>", html_report)
            self.assertIn("<strong>Scenario:</strong> Treasury reallocation dry run", html_report)
            self.assertIn("Recommendation: Proceed with revision", html_report)
            self.assertIn("DAO council", html_report)

    def test_list_presets_prints_supported_trait_groups(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--list-presets"],
            cwd=ROOT,
            env={**dict(), **{"PYTHONPATH": str(SRC)}},
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("community", result.stdout)
        self.assertIn("delegates", result.stdout)


if __name__ == "__main__":
    unittest.main()
