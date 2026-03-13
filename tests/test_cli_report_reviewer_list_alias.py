from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliReportReviewerListAliasTests(unittest.TestCase):
    def test_cli_accepts_report_reviewer_list_alias(self) -> None:
        scenario = {
            "proposal": "Ship a staged governance change.",
            "stakeholders": ["delegates", "community"],
            "report_reviewer_list": ["delegates", "ops reviewers"],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["scenario"]["report_reviewers"], "delegates, ops reviewers")


if __name__ == "__main__":
    unittest.main()
