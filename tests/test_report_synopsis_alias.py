from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportSynopsisAliasTests(unittest.TestCase):
    def test_report_synopsis_alias_populates_report_summary(self) -> None:
        scenario = {
            "proposal": "Stage the rollout.",
            "stakeholders": ["delegates"],
            "report": {"report_synopsis": "Keep the memo short and reviewer-ready."},
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**dict(__import__("os").environ), "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["scenario"]["report_summary"], "Keep the memo short and reviewer-ready.")


if __name__ == "__main__":
    unittest.main()
