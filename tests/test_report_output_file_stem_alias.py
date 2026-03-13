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


class ReportOutputFileStemAliasTests(unittest.TestCase):
    def test_report_outputs_output_file_stem_alias_sets_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            report_dir = Path(tmpdir) / "artifacts"
            scenario_path.write_text(
                """proposal: Prepare a reviewer-ready memo bundle.
stakeholders:
  - preset: dao
report:
  outputs:
    output_file_stem: reviewer-hand-off
""",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path), "--report-dir", str(report_dir)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "reviewer-hand-off")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "reviewer-hand-off")
            self.assertTrue((report_dir / "reviewer-hand-off.md").exists())
            self.assertTrue((report_dir / "reviewer-hand-off.html").exists())
            self.assertTrue((report_dir / "reviewer-hand-off.json").exists())

    def test_top_level_report_output_file_stem_alias_sets_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            report_dir = Path(tmpdir) / "artifacts"
            scenario_path.write_text(json.dumps({
                "proposal": "Ship one scenario-file replay with one named report trio.",
                "stakeholders": [{"preset": "delegates"}],
                "report_output_file_stem": "delegate-review-lane",
            }), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path), "--report-dir", str(report_dir)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "delegate-review-lane")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-review-lane")
            self.assertTrue((report_dir / "delegate-review-lane.md").exists())
            self.assertTrue((report_dir / "delegate-review-lane.html").exists())
            self.assertTrue((report_dir / "delegate-review-lane.json").exists())


if __name__ == "__main__":
    unittest.main()
