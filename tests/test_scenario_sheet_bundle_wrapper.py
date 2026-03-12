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


class ScenarioSheetBundleWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_sheet_bundle_wrapper_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario-sheet-bundle.yaml"
            scenario_path.write_text(
                """
scenario_sheet_bundle:
  scenario:
    name: Scenario sheet bundle rehearsal
    context: Replay one wrapped governance packet into the default report bundle.
  proposal:
    title: Treasury rehearsal gate
    summary: Require a lightweight simulation pass before execution.
    bullets:
      - Add a scenario review before on-chain submission.
      - Keep delegate objections visible in the saved memo.
  stakeholders:
    - name: Delegate circle
      preset: delegates
    - name: Treasury stewards
      preset: dao
  report:
    title: Scenario sheet bundle memo
""".strip(),
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
            self.assertEqual(payload["scenario"]["name"], "Scenario sheet bundle rehearsal")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario sheet bundle memo")
            self.assertEqual([item["preset"] for item in payload["responses"]], ["delegates", "dao"])


if __name__ == "__main__":
    unittest.main()
