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
CLI = [sys.executable, "-m", "governance_sandbox.cli", "run"]


class ReportPathShortAliasTests(unittest.TestCase):
    def test_run_supports_short_markdown_and_html_report_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a delegate-ready treasury checkpoint before the next vote.
stakeholders:
  - name: DAO council
    preset: dao
  - name: Builder guild
    preset: contributors
report:
  md_file: outputs/briefing.md
  html_output: outputs/briefing.html
  json_output: outputs/briefing.json
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                CLI + ["--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            artifacts = payload["report"]["artifacts"]
            outputs = scenario_path.parent / "outputs"
            self.assertEqual(Path(artifacts["json"]), (outputs / "briefing.json").resolve())
            self.assertEqual(Path(artifacts["markdown"]), (outputs / "briefing.md").resolve())
            self.assertEqual(Path(artifacts["html"]), (outputs / "briefing.html").resolve())
            self.assertTrue((outputs / "briefing.json").exists())
            self.assertTrue((outputs / "briefing.md").exists())
            self.assertTrue((outputs / "briefing.html").exists())


if __name__ == "__main__":
    unittest.main()
