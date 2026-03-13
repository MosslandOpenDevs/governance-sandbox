from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportDirectoryAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_directory_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """name: Governance alignment memo
proposal: Keep one scenario-file import tied to one named report directory alias.
stakeholders:
  - name: Treasury delegates
    preset: delegates
report_name: governance-alignment-pack
report_directory: exports/reports
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
            report_dir = scenario_path.parent / "exports" / "reports"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "governance-alignment-pack.json").exists())
            self.assertTrue((report_dir / "governance-alignment-pack.md").exists())
            self.assertTrue((report_dir / "governance-alignment-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
