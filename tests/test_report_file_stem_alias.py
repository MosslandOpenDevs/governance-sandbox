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


class ReportFileStemAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_file_stem_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            report_dir = Path(tmpdir) / "artifacts"
            scenario_path.write_text(
                """name: File stem alias rehearsal
proposal: Rebalance grants and growth campaigns while protecting contributor trust.
stakeholders:
  - preset: dao
  - preset: contributors
report_file_stem: delegate-review-pack
""",
                encoding="utf-8",
            )
            env = {**os.environ, "PYTHONPATH": str(SRC)}
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
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-review-pack")
            self.assertTrue((report_dir / "delegate-review-pack.md").exists())
            self.assertTrue((report_dir / "delegate-review-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
