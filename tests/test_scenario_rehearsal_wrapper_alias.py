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


class ScenarioRehearsalWrapperAliasTests(unittest.TestCase):
    def test_run_accepts_scenario_rehearsal_wrapper(self) -> None:
        scenario = {
            "scenario_rehearsal": {
                "name": "Delegate rehearsal wrapper",
                "proposal": "Ship a staged treasury review before the next delegate call.",
                "stakeholders": {
                    "DAO Ops": "dao",
                    "Lead Delegate": "delegate",
                },
                "report": {
                    "title": "Delegate rehearsal memo",
                },
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
        self.assertEqual(payload["scenario"]["name"], "Delegate rehearsal wrapper")
        self.assertEqual(payload["scenario"]["report_title"], "Delegate rehearsal memo")
        self.assertEqual([item["preset"] for item in payload["responses"]], ["dao", "delegates"])

    def test_readme_mentions_scenario_rehearsal_wrapper_note(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REHEARSAL_WRAPPER_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REHEARSAL_WRAPPER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
