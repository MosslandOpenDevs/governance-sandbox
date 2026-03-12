from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


class ReportBriefingAliasTest(unittest.TestCase):
    def test_run_supports_report_briefing_alias_for_report_summary(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_file = tmp_path / "scenario.json"
            scenario_file.write_text(
                json.dumps(
                    {
                        "proposal": "Stage treasury dashboard updates before the next vote.",
                        "stakeholders": ["delegates"],
                        "report": {
                            "title": "Briefing alias demo",
                            "briefing": "A short reviewer-facing memo summary carried through markdown and html outputs.",
                        },
                    }
                ),
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
                "A short reviewer-facing memo summary carried through markdown and html outputs.",
            )


if __name__ == "__main__":
    unittest.main()
