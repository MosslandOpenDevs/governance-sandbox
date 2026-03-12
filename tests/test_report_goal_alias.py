from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportGoalAliasTests(unittest.TestCase):
    def test_run_accepts_report_goal_alias_for_markdown_summary(self) -> None:
        payload = {
            "proposal": "Ship a delegated treasury policy review before the next vote.",
            "stakeholders": ["DAO operators", "Delegate council"],
            "report": {"goal": "Give reviewers a one-screen memo before the dry run."},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            report_path = Path(tmpdir) / "report.md"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-markdown",
                    str(report_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=Path(__file__).resolve().parents[1],
            )

            result = json.loads(completed.stdout)
            report_text = report_path.read_text(encoding="utf-8")

        self.assertEqual(result["scenario"]["report_summary"], "Give reviewers a one-screen memo before the dry run.")
        self.assertIn("## Report summary", report_text)
        self.assertIn("Give reviewers a one-screen memo before the dry run.", report_text)


if __name__ == "__main__":
    unittest.main()
