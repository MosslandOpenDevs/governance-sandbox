from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportBundleDirectoryAliasTests(unittest.TestCase):
    def test_run_accepts_bundle_directory_alias_for_report_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps({
                "proposal": "Load one scenario file and render one named report bundle.",
                "stakeholders": [{"name": "DAO Council", "preset": "dao"}],
                "report_outputs": {
                    "bundle_directory": "bundles",
                    "basename": "scenario-bundle",
                },
            }), encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            bundle_dir = scenario_path.parent / "bundles"
            artifacts = payload["report"]["artifacts"]
            self.assertEqual(Path(artifacts["directory"]), bundle_dir.resolve())
            self.assertEqual(Path(artifacts["markdown"]), (bundle_dir / "scenario-bundle.md").resolve())
            self.assertTrue((bundle_dir / "scenario-bundle.html").exists())


if __name__ == "__main__":
    unittest.main()
