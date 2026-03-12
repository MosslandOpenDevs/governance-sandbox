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


class ReportOutputFileAliasesTests(unittest.TestCase):
    def test_run_supports_direct_report_output_aliases_on_scenario_root(self) -> None:
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
report_json_output: outputs/root-report.json
report_md_output: outputs/root-report.md
report_html_output: outputs/root-report.html
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
            self.assertEqual(Path(artifacts["json"]), (outputs / "root-report.json").resolve())
            self.assertEqual(Path(artifacts["markdown"]), (outputs / "root-report.md").resolve())
            self.assertEqual(Path(artifacts["html"]), (outputs / "root-report.html").resolve())
            self.assertTrue((outputs / "root-report.json").exists())
            self.assertTrue((outputs / "root-report.md").exists())
            self.assertTrue((outputs / "root-report.html").exists())


if __name__ == "__main__":
    unittest.main()
