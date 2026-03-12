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


class ReportBlurbAliasTests(unittest.TestCase):
    def test_run_accepts_report_blurb_alias(self) -> None:
        payload = {
            "proposal": "Launch a delegate office hours pilot.",
            "stakeholders": ["community"],
            "report": {"report_blurb": "Share a concise reviewer-facing summary."}
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path), "--report-markdown", str(Path(tmpdir) / "report.md")],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            report_text = (Path(tmpdir) / "report.md").read_text(encoding="utf-8")

        result = json.loads(completed.stdout)
        self.assertEqual(result["scenario"]["report_summary"], "Share a concise reviewer-facing summary.")
        self.assertIn("## Report summary", report_text)
        self.assertIn("Share a concise reviewer-facing summary.", report_text)


if __name__ == "__main__":
    unittest.main()
