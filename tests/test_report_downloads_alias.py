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


class ReportDownloadsAliasTests(unittest.TestCase):
    def test_run_supports_report_outputs_downloads_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario:
  name: Downloads alias rehearsal
report:
  outputs:
    downloads:
      json: artifacts/downloads/rehearsal.json
      markdown: artifacts/downloads/rehearsal.md
      html: artifacts/downloads/rehearsal.html
inputs:
  proposal: Add milestone checkpoints before treasury releases.
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
            report_root = scenario_path.parent / "artifacts" / "downloads"
            self.assertEqual(payload["report"]["artifacts"]["json"], str((report_root / "rehearsal.json").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str((report_root / "rehearsal.md").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["html"], str((report_root / "rehearsal.html").resolve()))
            self.assertTrue((report_root / "rehearsal.json").exists())
            self.assertTrue((report_root / "rehearsal.md").exists())
            self.assertTrue((report_root / "rehearsal.html").exists())


if __name__ == "__main__":
    unittest.main()
