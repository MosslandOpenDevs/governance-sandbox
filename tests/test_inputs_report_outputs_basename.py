from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InputsReportOutputsBasenameTests(unittest.TestCase):
    def test_inputs_report_outputs_basename_drives_report_dir_bundle_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "artifacts"
            scenario_path.write_text(
                """
scenario:
  name: Delegate readiness review
inputs:
  proposal: Launch a staged delegate briefing pack.
  stakeholders:
    - name: DAO core
      preset: dao
    - name: Community delegates
      preset: delegates
  report:
    outputs:
      basename: Delegate Packet
""".strip()
                + "\n",
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
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-packet")
            self.assertTrue((report_dir / "delegate-packet.json").exists())
            self.assertTrue((report_dir / "delegate-packet.md").exists())
            self.assertTrue((report_dir / "delegate-packet.html").exists())


if __name__ == "__main__":
    unittest.main()
