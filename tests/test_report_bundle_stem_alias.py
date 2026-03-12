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


class GovernanceSandboxReportBundleStemAliasTests(unittest.TestCase):
    def test_report_outputs_bundle_stem_alias_drives_bundle_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """proposal: Publish a shorter review packet before the vote.
stakeholders:
  - name: Delegate circle
    preset: delegates
report:
  outputs:
    bundle_stem: review-packet
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
            self.assertEqual(payload["scenario"]["report_basename"], "review-packet")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "review-packet")
            self.assertTrue((report_dir / "review-packet.md").exists())
            self.assertTrue((report_dir / "review-packet.html").exists())
            self.assertTrue((report_dir / "review-packet.json").exists())


if __name__ == "__main__":
    unittest.main()
