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


class GovernanceSandboxReportBundleBasenameAliasTests(unittest.TestCase):
    def test_report_outputs_bundle_basename_alias_drives_bundle_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "reports"
            scenario_path.write_text(
                """proposal: Ship a staged governance dry run before the formal vote.
stakeholders:
  - name: DAO council
    preset: dao
report:
  title: Dry-run packet
  outputs:
    bundle_basename: dry-run-packet
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "dry-run-packet")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "dry-run-packet")
            self.assertTrue((report_dir / "dry-run-packet.json").exists())
            self.assertTrue((report_dir / "dry-run-packet.md").exists())
            self.assertTrue((report_dir / "dry-run-packet.html").exists())


if __name__ == "__main__":
    unittest.main()
