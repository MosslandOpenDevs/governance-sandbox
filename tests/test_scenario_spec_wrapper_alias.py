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


class ScenarioSpecWrapperAliasTests(unittest.TestCase):
    def test_run_supports_scenario_spec_wrapper_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario_spec:
  name: Scenario spec wrapper rehearsal
  proposal: Publish the treasury rehearsal pack before the next delegate call.
  stakeholders:
    - name: Delegate council
      preset: delegates
    - name: Community stewards
      preset: community
  report:
    title: Scenario spec wrapper memo
    summary: Scenario spec wrapper proving YAML scenario import plus report metadata handoff.
""",
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
            self.assertEqual(payload["scenario"]["name"], "Scenario spec wrapper rehearsal")
            self.assertEqual(payload["scenario"]["report_title"], "Scenario spec wrapper memo")
            self.assertEqual(payload["scenario"]["report_summary"], "Scenario spec wrapper proving YAML scenario import plus report metadata handoff.")
            self.assertEqual([response["preset"] for response in payload["responses"]], ["delegates", "community"])


if __name__ == "__main__":
    unittest.main()
