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


class ReportDirectoryPluralAliasTests(unittest.TestCase):
    def test_run_supports_plural_report_directory_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Ship one replayable governance memo bundle for delegates.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  outputs:
    reports_dir: exports/reports
    basename: delegate-review
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
            report_dir = scenario_path.parent / "exports" / "reports"
            artifacts = payload["report"]["artifacts"]
            self.assertEqual(Path(artifacts["directory"]), report_dir.resolve())
            self.assertEqual(Path(artifacts["json"]), (report_dir / "delegate-review.json").resolve())
            self.assertEqual(Path(artifacts["markdown"]), (report_dir / "delegate-review.md").resolve())
            self.assertEqual(Path(artifacts["html"]), (report_dir / "delegate-review.html").resolve())
            self.assertTrue((report_dir / "delegate-review.json").exists())
            self.assertTrue((report_dir / "delegate-review.md").exists())
            self.assertTrue((report_dir / "delegate-review.html").exists())


if __name__ == "__main__":
    unittest.main()
