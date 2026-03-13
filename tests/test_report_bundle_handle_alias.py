from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportBundleHandleAliasTests(unittest.TestCase):
    def test_run_accepts_report_bundle_handle_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: |
  Publish a governance rehearsal memo.
stakeholders:
  - name: Delegate circle
    preset: delegates
report:
  outputs:
    bundle_handle: rehearsal-handle
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
            self.assertEqual(payload["report"]["artifacts"]["basename"], "rehearsal-handle")

    def test_run_accepts_top_level_report_bundle_handle_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Publish a governance rehearsal memo.",
                        "stakeholders": [{"name": "Delegate circle", "preset": "delegates"}],
                        "report_bundle_handle": "top-level-handle",
                    }
                ),
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
            self.assertEqual(payload["report"]["artifacts"]["basename"], "top-level-handle")
