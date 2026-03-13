from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportBundleSlugAliasTests(unittest.TestCase):
    def test_run_supports_report_bundle_slug_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            report_dir = tmp / "reports"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Fund a delegate education sprint.",
                        "stakeholders": ["dao", "delegates", "community"],
                        "report_bundle_slug": "delegate-education-sprint",
                        "report_dir": str(report_dir),
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "delegate-education-sprint")
            self.assertTrue((report_dir / "delegate-education-sprint.md").exists())
            self.assertTrue((report_dir / "delegate-education-sprint.html").exists())
            self.assertTrue((report_dir / "delegate-education-sprint.json").exists())


if __name__ == "__main__":
    unittest.main()
