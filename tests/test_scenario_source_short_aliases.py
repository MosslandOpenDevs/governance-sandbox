from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScenarioSourceShortAliasesTest(unittest.TestCase):
    def test_scenario_src_alias_flows_into_report_metadata(self) -> None:
        scenario = {
            "proposal": "Ship a contributor grants policy with staged treasury reporting.",
            "stakeholders": ["DAO", "Delegates"],
            "scenario_src": "fixtures/contributor-grants.yaml",
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
        self.assertEqual(payload["scenario"]["scenario_file"], "fixtures/contributor-grants.yaml")
        self.assertEqual(payload["report"]["scenario_file"], "fixtures/contributor-grants.yaml")

    def test_source_href_alias_flows_into_report_metadata(self) -> None:
        scenario = {
            "proposal": "Expand delegate review windows before treasury votes.",
            "stakeholders": {"Delegate Guild": "delegates", "Community": "community"},
            "source_href": "https://example.com/scenarios/delegate-review.yaml",
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
        self.assertEqual(payload["scenario"]["scenario_file"], "https://example.com/scenarios/delegate-review.yaml")
        self.assertEqual(payload["report"]["scenario_file"], "https://example.com/scenarios/delegate-review.yaml")


if __name__ == "__main__":
    unittest.main()
