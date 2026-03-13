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


class ReportOutputLabelTopLevelAliasTests(unittest.TestCase):
    def test_top_level_report_output_label_sets_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "reports"
            scenario_path.write_text(
                f"""proposal: Approve a staged delegate feedback pilot.
stakeholders:
  - name: Delegates
    preset: delegates
report_output_label: Delegate Feedback Bundle
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
            self.assertEqual(payload["scenario"]["report_basename"], "Delegate Feedback Bundle")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-feedback-bundle")
            self.assertTrue((report_dir / "delegate-feedback-bundle.json").exists())
            self.assertTrue((report_dir / "delegate-feedback-bundle.md").exists())
            self.assertTrue((report_dir / "delegate-feedback-bundle.html").exists())


if __name__ == "__main__":
    unittest.main()
