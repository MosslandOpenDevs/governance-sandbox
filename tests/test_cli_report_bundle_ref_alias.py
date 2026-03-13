from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportBundleRefAliasTest(unittest.TestCase):
    def test_report_bundle_ref_alias_sets_report_basename(self) -> None:
        scenario = {
            "proposal": "Pilot a treasury transparency dashboard before the next DAO vote.",
            "stakeholders": {"Treasury Council": "dao", "Delegates": "delegates"},
            "report_bundle_ref": "Treasury Transparency Memo",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["report"]["artifacts"]["basename"], "treasury-transparency-memo")


if __name__ == "__main__":
    unittest.main()
