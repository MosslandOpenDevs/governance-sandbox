from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NestedScenarioInputsSourceShortAliasesTests(unittest.TestCase):
    def _run(self, payload: dict[str, object]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.json"
            report_dir = Path(tmpdir) / "reports"
            payload.setdefault("report", {"outputs": {"dir": str(report_dir)}})
            scenario.write_text(json.dumps(payload), encoding="utf-8")
            proc = subprocess.run(["python3", "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario)], cwd=ROOT, capture_output=True, text=True, check=True)
            return json.loads(proc.stdout)

    def test_nested_inputs_accept_scenario_src_from_stdin(self) -> None:
        payload = {"inputs": {"proposal": "Ship treasury dashboard", "stakeholders": [{"name": "Core team", "stance": "supportive"}], "scenario_src": "fixtures/demo-scenario.yaml"}}
        proc = subprocess.run(["python3", "-m", "governance_sandbox.cli", "run", "--scenario-file", "-"], cwd=ROOT, input=json.dumps(payload), capture_output=True, text=True, check=True)
        result = json.loads(proc.stdout)
        self.assertEqual(result["scenario"]["scenario_file"], "fixtures/demo-scenario.yaml")

    def test_nested_scenario_inputs_accept_source_href_from_stdin(self) -> None:
        payload = {"scenario_inputs": {"proposal": "Ship treasury dashboard", "stakeholders": [{"name": "Delegates", "stance": "cautious"}], "source_href": "https://example.com/scenarios/dao.json"}}
        proc = subprocess.run(["python3", "-m", "governance_sandbox.cli", "run", "--scenario-file", "-"], cwd=ROOT, input=json.dumps(payload), capture_output=True, text=True, check=True)
        result = json.loads(proc.stdout)
        self.assertEqual(result["scenario"]["scenario_file"], "https://example.com/scenarios/dao.json")


if __name__ == "__main__":
    unittest.main()
