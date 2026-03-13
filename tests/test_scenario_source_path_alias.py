from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScenarioSourcePathAliasTest(unittest.TestCase):
    def test_source_path_alias_flows_into_report_metadata(self) -> None:
        scenario = {
            "proposal": "Generate markdown and html reports from one imported governance scenario.",
            "stakeholders": {"Delegate Circle": "delegates", "Community": "community"},
            "source_path": "fixtures/source-path-demo.yaml",
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
        self.assertEqual(payload["scenario"]["scenario_file"], "fixtures/source-path-demo.yaml")
        self.assertEqual(payload["report"]["scenario_file"], "fixtures/source-path-demo.yaml")


if __name__ == "__main__":
    unittest.main()
