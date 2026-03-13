from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


class ReportExecutiveSummaryAliasTest(unittest.TestCase):
    def test_run_supports_top_level_executive_summary_alias_for_report_summary(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_file = tmp_path / "scenario.yaml"
            scenario_file.write_text(
                """
proposal: Ship an onboarding checklist before the next governance vote.
stakeholders:
  - community
executive_summary: Keep one reviewer-facing memo summary visible in markdown and html outputs.
""".strip(),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_file),
                ],
                cwd=Path(__file__).resolve().parents[1],
                env={**os.environ, "PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(
                payload["scenario"]["report_summary"],
                "Keep one reviewer-facing memo summary visible in markdown and html outputs.",
            )


if __name__ == "__main__":
    unittest.main()
