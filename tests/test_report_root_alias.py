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


class ReportRootAliasTests(unittest.TestCase):
    def test_run_accepts_report_root_alias_in_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a treasury checkpoint memo.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  outputs:
    report_root: reports
    basename: checkpoint-memo
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
            report_dir = scenario_path.parent / "reports"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "checkpoint-memo.json").exists())
            self.assertTrue((report_dir / "checkpoint-memo.md").exists())
            self.assertTrue((report_dir / "checkpoint-memo.html").exists())


if __name__ == "__main__":
    unittest.main()
