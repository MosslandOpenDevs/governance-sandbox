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


class ReportBundleTitleAliasTests(unittest.TestCase):
    def test_run_supports_report_bundle_title_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "reports"
            scenario_path.write_text(
                """proposal: Approve a staged community grants reboot.
stakeholders:
  - name: Community delegates
    preset: delegates
report_bundle_title: Community Grants Reboot Pack
report_dir: {report_dir}
""".format(report_dir=report_dir),
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
            self.assertEqual(payload["scenario"]["report_basename"], "Community Grants Reboot Pack")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "community-grants-reboot-pack")
            self.assertTrue((report_dir / "community-grants-reboot-pack.json").exists())
            self.assertTrue((report_dir / "community-grants-reboot-pack.md").exists())
            self.assertTrue((report_dir / "community-grants-reboot-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
