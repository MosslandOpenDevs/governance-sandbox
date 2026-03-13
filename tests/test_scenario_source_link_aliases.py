from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScenarioSourceLinkAliasesTest(unittest.TestCase):
    def test_scenario_link_alias_flows_into_report_metadata(self) -> None:
        scenario = {
            "proposal": "Ship one scenario-file replay before widening the governance demo.",
            "stakeholders": ["DAO", "Community"],
            "scenario_link": "https://example.com/scenarios/demo-governance.yaml",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["scenario"]["scenario_file"], "https://example.com/scenarios/demo-governance.yaml")
        self.assertEqual(payload["report"]["scenario_file"], "https://example.com/scenarios/demo-governance.yaml")

    def test_source_link_alias_flows_into_report_metadata(self) -> None:
        scenario = {
            "proposal": "Keep markdown and html report output visible from the same scenario import.",
            "stakeholders": {"Delegates": "delegates", "Investors": "investors"},
            "source_link": "fixtures/investor-review.yaml",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["scenario"]["scenario_file"], "fixtures/investor-review.yaml")
        self.assertEqual(payload["report"]["scenario_file"], "fixtures/investor-review.yaml")


if __name__ == "__main__":
    unittest.main()
