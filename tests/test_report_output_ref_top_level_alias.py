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


class ReportOutputRefTopLevelAliasTests(unittest.TestCase):
    def test_top_level_report_output_ref_sets_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "reports"
            scenario_path.write_text(
                f"""proposal: Approve a staged delegate feedback pilot.
stakeholders:
  - name: Delegates
    preset: delegates
report_output_ref: delegate-feedback-ref
report_dir: {report_dir}
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
            self.assertEqual(payload["scenario"]["report_basename"], "delegate-feedback-ref")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-feedback-ref")
            self.assertTrue((report_dir / "delegate-feedback-ref.json").exists())
            self.assertTrue((report_dir / "delegate-feedback-ref.md").exists())
            self.assertTrue((report_dir / "delegate-feedback-ref.html").exists())


if __name__ == "__main__":
    unittest.main()
