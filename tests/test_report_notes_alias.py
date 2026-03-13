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


class GovernanceSandboxReportNotesAliasTests(unittest.TestCase):
    def test_run_supports_report_notes_alias_in_scenario_file(self) -> None:
        scenario = """
proposal: Publish a treasury checkpoint memo before execution.
stakeholders:
  - name: Delegate circle
    preset: delegates
report:
  report_notes: Keep the memo short, reviewer-ready, and exportable.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(scenario, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload["scenario"]["report_summary"],
            "Keep the memo short, reviewer-ready, and exportable.",
        )


if __name__ == "__main__":
    unittest.main()
