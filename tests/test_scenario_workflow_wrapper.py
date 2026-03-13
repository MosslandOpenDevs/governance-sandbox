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


class ScenarioWorkflowWrapperTests(unittest.TestCase):
    def test_scenario_workflow_wrapper_is_supported(self) -> None:
        scenario = {
            "scenario_workflow": {
                "proposal": {
                    "title": "Automate treasury alerts",
                    "summary": "Stage one governance automation before rollout.",
                },
                "stakeholders": {"DAO Ops": "dao", "Delegate Circle": "delegates"},
                "report": {"title": "Treasury alert workflow memo"},
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
        self.assertEqual(payload["scenario"]["report_title"], "Treasury alert workflow memo")
        self.assertEqual([item["preset"] for item in payload["responses"]], ["dao", "delegates"])

    def test_readme_mentions_scenario_workflow_wrapper_support(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("scenario_workflow", readme)
        self.assertIn("scenario_workflow_bundle", readme)


if __name__ == "__main__":
    unittest.main()
