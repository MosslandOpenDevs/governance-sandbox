from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportFollowUpAliasTests(unittest.TestCase):
    def test_run_supports_report_follow_up_alias_in_markdown_and_html(self) -> None:
        scenario_text = textwrap.dedent(
            """
            proposal: Ship scenario-file report bundles
            stakeholders:
              - name: Delegate A
                stance: support
                influence: 4
                note: Wants machine and human artifacts together.
            report:
              report_follow_up: Reopen the shared markdown and html report before forum posting.
            """
        ).strip()

        with tempfile.TemporaryDirectory() as tmp:
            scenario_path = Path(tmp) / "scenario.yaml"
            report_dir = Path(tmp) / "reports"
            scenario_path.write_text(scenario_text, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                capture_output=True,
                text=True,
                env={**__import__("os").environ, "PYTHONPATH": str(SRC)},
                check=True,
            )

            payload = json.loads(result.stdout)
            markdown_path = report_dir / f"{payload['report']['artifacts']['basename']}.md"
            html_path = report_dir / f"{payload['report']['artifacts']['basename']}.html"

            self.assertEqual(
                payload["scenario"]["report_summary"],
                "Reopen the shared markdown and html report before forum posting.",
            )
            self.assertIn(
                "Reopen the shared markdown and html report before forum posting.",
                markdown_path.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Reopen the shared markdown and html report before forum posting.",
                html_path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
