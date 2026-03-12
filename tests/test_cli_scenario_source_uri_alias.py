from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScenarioSourceUriAliasTest(unittest.TestCase):
    def test_scenario_source_uri_alias_flows_into_report_metadata(self) -> None:
        scenario = {
            "proposal": "Ship a delegated grants pilot with clear budget caps.",
            "stakeholders": {
                "Treasury Council": "dao",
                "Delegate Desk": "delegates",
            },
            "scenario_uri": "https://example.com/scenarios/delegated-grants.yaml",
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
        self.assertEqual(
            payload["scenario"]["scenario_file"],
            "https://example.com/scenarios/delegated-grants.yaml",
        )
        self.assertEqual(
            payload["report"]["scenario_file"],
            "https://example.com/scenarios/delegated-grants.yaml",
        )


if __name__ == "__main__":
    unittest.main()
