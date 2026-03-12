from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
README_PATH = ROOT / "README.md"


class ScenarioPlanWrapperAliasTests(unittest.TestCase):
    def test_scenario_plan_wrapper_is_supported(self) -> None:
        scenario = {
            "scenario_plan": {
                "proposal": {"title": "Treasury reporting pilot", "summary": "Ship a monthly report."},
                "stakeholders": {"DAO Ops": "dao", "Lead Delegate": "delegate"},
                "report": {"title": "Monthly reporting memo"},
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["scenario"]["report_title"], "Monthly reporting memo")
        self.assertEqual([item["preset"] for item in payload["responses"]], ["dao", "delegates"])

    def test_readme_mentions_scenario_plan_wrapper_note(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_SCENARIO_PLAN_WRAPPER_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "GOVERNANCE_SANDBOX_SCENARIO_PLAN_WRAPPER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
