from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class ReportSlugAliasTests(unittest.TestCase):
    def test_scenario_report_slug_alias_drives_bundle_basename(self) -> None:
        root = Path(__file__).resolve().parents[1]
        scenario = {
            "proposal": "Ship a governance dashboard for delegates and contributors.",
            "stakeholders": ["DAO delegate", "core contributor"],
            "report": {"title": "Governance Dashboard Review"},
            "report_slug": "delegate-dashboard-review",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            report_dir = Path(tmpdir) / "reports"
            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=root,
                env={**__import__("os").environ, "PYTHONPATH": str(root / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            artifacts = payload["report"]["artifacts"]

            self.assertEqual(artifacts["basename"], "delegate-dashboard-review")
            self.assertTrue((report_dir / "delegate-dashboard-review.json").exists())
            self.assertTrue((report_dir / "delegate-dashboard-review.md").exists())
            self.assertTrue((report_dir / "delegate-dashboard-review.html").exists())


if __name__ == "__main__":
    unittest.main()
