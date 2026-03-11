from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportOutputDirectoryAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_output_directory_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """name: Treasury runway check
context: Verify one top-level report_output_directory alias.
proposal: Keep the report bundle generated from one top-level alias.
stakeholders:
  - name: Delegate bench
    preset: delegates
report_name: delegate-ops-pack
report_output_directory: exports/bundles
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
            report_dir = scenario_path.parent / "exports" / "bundles"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "delegate-ops-pack.json").exists())
            self.assertTrue((report_dir / "delegate-ops-pack.md").exists())
            self.assertTrue((report_dir / "delegate-ops-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
