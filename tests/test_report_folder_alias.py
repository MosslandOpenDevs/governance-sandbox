from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportFolderAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_folder_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """name: Community grant refresh
proposal: Refresh the grants review process with a tighter review lane.
stakeholders:
  - name: Community council
    preset: community
report_name: grants-review-pack
report_folder: outputs/reports
""",
                encoding="utf-8",
            )

            env = dict(__import__("os").environ)
            env["PYTHONPATH"] = str(ROOT / "src")
            proc = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(proc.stdout)
            report_dir = scenario_path.parent / "outputs" / "reports"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "grants-review-pack.json").exists())
            self.assertTrue((report_dir / "grants-review-pack.md").exists())
            self.assertTrue((report_dir / "grants-review-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
