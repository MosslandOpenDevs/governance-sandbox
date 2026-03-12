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


class ReportPathsAliasesTests(unittest.TestCase):
    def test_run_accepts_report_paths_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            json_path = tmp / "artifacts" / "memo.json"
            markdown_path = tmp / "artifacts" / "memo.md"
            html_path = tmp / "artifacts" / "memo.html"
            scenario_path.write_text(
                f"""proposal: Keep the treasury communications upgrade on schedule.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  outputs:
    basename: report-paths-aliases
    paths:
      json: {json_path}
      markdown: {markdown_path}
      html: {html_path}
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "report-paths-aliases")
            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())


if __name__ == "__main__":
    unittest.main()
