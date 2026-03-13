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


class TopLevelReportDownloadsAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_downloads_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario:
  name: Top-level report downloads alias rehearsal
report_downloads:
  json: artifacts/top-level/rehearsal.json
  markdown: artifacts/top-level/rehearsal.md
  html: artifacts/top-level/rehearsal.html
inputs:
  proposal: Ship staged delegate messaging before the treasury vote.
  stakeholders:
    - name: Delegate circle
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            report_root = scenario_path.parent / "artifacts" / "top-level"
            self.assertEqual(payload["report"]["artifacts"]["json"], str((report_root / "rehearsal.json").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str((report_root / "rehearsal.md").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["html"], str((report_root / "rehearsal.html").resolve()))
            self.assertTrue((report_root / "rehearsal.json").exists())
            self.assertTrue((report_root / "rehearsal.md").exists())
            self.assertTrue((report_root / "rehearsal.html").exists())


if __name__ == "__main__":
    unittest.main()
