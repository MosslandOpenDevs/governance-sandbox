from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportBundleAliasTests(unittest.TestCase):
    def test_run_accepts_top_level_report_bundle_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Publish a governance rehearsal memo.",
                        "stakeholders": [{"name": "Delegate circle", "preset": "delegates"}],
                        "report_bundle_alias": "alias-bundle",
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "alias-bundle")

    def test_readme_mentions_report_bundle_alias(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("report_bundle_alias", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_BUNDLE_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
