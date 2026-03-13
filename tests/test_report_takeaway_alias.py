from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportTakeawayAliasTests(unittest.TestCase):
    def test_run_accepts_report_takeaway_alias_for_markdown_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = {
                "proposal": "Ship scenario-driven markdown reports before the governance vote.",
                "report": {"report_takeaway": "Give reviewers one clear takeaway before opening the JSON bundle."},
                "stakeholders": [
                    {"name": "DAO delegate", "stance": "support", "weight": 0.7},
                    {"name": "Community member", "stance": "mixed", "weight": 0.3},
                ],
            }
            scenario_path = Path(tmpdir) / "scenario.json"
            report_path = Path(tmpdir) / "report.md"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path), "--report-markdown", str(report_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
            report_text = report_path.read_text(encoding="utf-8")

        output = json.loads(result.stdout)
        self.assertEqual(output["scenario"]["report_summary"], "Give reviewers one clear takeaway before opening the JSON bundle.")
        self.assertIn("## Report summary", report_text)
        self.assertIn("Give reviewers one clear takeaway before opening the JSON bundle.", report_text)


if __name__ == "__main__":
    unittest.main()
