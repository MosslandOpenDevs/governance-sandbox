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


class ReportDescriptionAliasTests(unittest.TestCase):
    def test_run_accepts_report_description_alias(self) -> None:
        payload = {
            "proposal": "Create a delegate onboarding track with milestone-based reviews.",
            "stakeholders": ["delegates"],
            "report": {"report_description": "Delegate-ready memo summary for the first scenario-file report bundle."},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            markdown_path = Path(tmpdir) / "report.md"
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
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            report_text = markdown_path.read_text(encoding="utf-8")

        result = json.loads(completed.stdout)
        self.assertEqual(
            result["scenario"]["report_summary"],
            "Delegate-ready memo summary for the first scenario-file report bundle.",
        )
        self.assertIn("## Report summary", report_text)
        self.assertIn("Delegate-ready memo summary for the first scenario-file report bundle.", report_text)


if __name__ == "__main__":
    unittest.main()
