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


class ReportAudienceAliasTests(unittest.TestCase):
    def test_run_supports_top_level_audience_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """name: Audience alias rehearsal
proposal: Stage a contributor review before the final treasury post.
audience:
  - delegates
  - contributors
stakeholders:
  - name: Delegate pod
    preset: delegates
""",
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_audience"], "delegates, contributors")
            self.assertIn("## Report audience\ndelegates, contributors", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()


    def test_run_supports_nested_report_readers_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "reports"
            scenario_path.write_text(
                """proposal: Add a delegate review checkpoint before treasury deployment.
stakeholders:
  - delegates
  - contributors
report:
  report_readers:
    - forum reviewers
    - treasury stewards
  output_dir: reports
""",
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
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            markdown_path = report_dir / "governance-sandbox-report.md"
            html_path = report_dir / "governance-sandbox-report.html"

            self.assertEqual(payload["scenario"]["report_audience"], "forum reviewers, treasury stewards")
            self.assertIn("## Report audience\nforum reviewers, treasury stewards", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("<strong>Report audience:</strong> forum reviewers, treasury stewards", html_path.read_text(encoding="utf-8"))
