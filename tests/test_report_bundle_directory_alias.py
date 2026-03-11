from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportBundleDirectoryAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_bundle_directory_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "name": "DAO report bundle replay",
                        "proposal": "Ship one scenario-file-first report bundle for DAO reviewers.",
                        "stakeholders": [{"name": "DAO council", "preset": "dao"}],
                        "report_name": "dao-review-pack",
                        "report_bundle_directory": "exports/report-bundles",
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
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
            report_dir = scenario_path.parent / "exports" / "report-bundles"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "dao-review-pack.json").exists())
            self.assertTrue((report_dir / "dao-review-pack.md").exists())
            self.assertTrue((report_dir / "dao-review-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
