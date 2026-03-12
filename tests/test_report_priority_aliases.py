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


class ReportPriorityAliasTests(unittest.TestCase):
    def test_report_priority_alias_renders_in_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            scenario_path.write_text(
                """proposal: Stage the treasury automation rollout behind a governance checkpoint.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  title: Treasury checkpoint memo
  priority: High priority before Monday vote
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
                    "--report-html",
                    str(html_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_priority"], "High priority before Monday vote")
            markdown = markdown_path.read_text(encoding="utf-8")
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("## Report priority", markdown)
            self.assertIn("High priority before Monday vote", markdown)
            self.assertIn("<strong>Report priority:</strong> High priority before Monday vote", html)


if __name__ == "__main__":
    unittest.main()
