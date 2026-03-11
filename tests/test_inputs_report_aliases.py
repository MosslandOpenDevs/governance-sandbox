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


class InputsReportAliasTests(unittest.TestCase):
    def test_run_supports_nested_inputs_report_metadata_and_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """inputs:
  proposal: Publish a delegate-ready treasury checkpoint before the next vote.
  stakeholders:
    - name: DAO council
      preset: dao
    - name: Builder guild
      preset: contributors
  report:
    title: Inputs report memo
    summary: Nested inputs report metadata should drive the report bundle.
    audience:
      - delegates
      - contributors
    output_name: inputs-report-bundle
    directory: outputs
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            report_dir = scenario_path.parent / "outputs"
            self.assertEqual(payload["scenario"]["report_title"], "Inputs report memo")
            self.assertEqual(payload["scenario"]["report_summary"], "Nested inputs report metadata should drive the report bundle.")
            self.assertEqual(payload["scenario"]["report_audience"], "delegates, contributors")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "inputs-report-bundle")
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "inputs-report-bundle.json").exists())
            self.assertTrue((report_dir / "inputs-report-bundle.md").exists())
            self.assertTrue((report_dir / "inputs-report-bundle.html").exists())


if __name__ == "__main__":
    unittest.main()
