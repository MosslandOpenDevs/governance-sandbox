import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


class ReportOutputLabelAliasTests(unittest.TestCase):
    def test_report_output_label_alias_drives_bundle_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "exports"
            scenario_path.write_text(
                """proposal: Publish a governance rehearsal memo before the vote.
stakeholders:
  - name: Delegate Circle
    preset: delegates
report:
  output_label: delegate-ready-review
""",
                encoding="utf-8",
            )

            completed = subprocess.run(
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
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "delegate-ready-review")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-ready-review")
            self.assertTrue((report_dir / "delegate-ready-review.json").exists())
            self.assertTrue((report_dir / "delegate-ready-review.md").exists())
            self.assertTrue((report_dir / "delegate-ready-review.html").exists())


if __name__ == "__main__":
    unittest.main()
