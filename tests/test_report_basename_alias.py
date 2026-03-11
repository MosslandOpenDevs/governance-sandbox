from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportBasenameAliasTests(unittest.TestCase):
    def test_report_output_name_alias_drives_report_dir_bundle_names(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            report_dir = Path(tmpdir) / "artifacts"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Ship a staged treasury reporting upgrade.",
                        "stakeholders": [
                            {"name": "DAO", "preset": "dao"},
                            {"name": "Delegates", "preset": "delegates"},
                        ],
                        "report": {
                            "output_name": "Delegate Ready Bundle",
                        },
                    }
                ),
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
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONPATH": str(root / "src")},
            )

            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-ready-bundle")
            self.assertTrue((report_dir / "delegate-ready-bundle.json").exists())
            self.assertTrue((report_dir / "delegate-ready-bundle.md").exists())
            self.assertTrue((report_dir / "delegate-ready-bundle.html").exists())
            self.assertTrue((report_dir / "report.json").exists())
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
