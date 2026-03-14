from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProposalFileAliasCliTest(unittest.TestCase):
    def test_proposal_file_alias_loads_scenario_and_report_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """
proposal: Launch a delegate budget review pilot.
stakeholders:
  - DAO council
  - delegates
report:
  outputs:
    basename: pilot-review
""".strip()
                + "\n",
                encoding="utf-8",
            )
            report_md = tmp / "out.md"
            report_html = tmp / "out.html"
            command = [
                sys.executable,
                "-m",
                "governance_sandbox.cli",
                "run",
                "--proposal-file",
                str(scenario_path),
                "--report-markdown-file",
                str(report_md),
                "--report-html-file",
                str(report_html),
            ]
            completed = subprocess.run(
                command,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["report"]["scenario_format"], "yaml")
            self.assertTrue(report_md.exists())
            self.assertTrue(report_html.exists())
            self.assertIn("Governance Sandbox Report", report_md.read_text(encoding="utf-8"))
            self.assertEqual(payload["report"]["artifacts"]["html"], str(report_html.resolve()))
            self.assertEqual(payload["report"]["artifacts"]["basename"], "pilot-review")


if __name__ == "__main__":
    unittest.main()
