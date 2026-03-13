from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioLabelAliasTests(unittest.TestCase):
    def test_scenario_label_alias(self) -> None:
        tmp_dir = ROOT / ".tmp-test-scenario-label"
        tmp_dir.mkdir(exist_ok=True)
        scenario_file = tmp_dir / "scenario-label.json"
        scenario_file.write_text(
            json.dumps(
                {
                    "scenario_label": "Delegates Roundtable",
                    "proposal": "Adopt phased treasury reporting.",
                    "stakeholders": ["delegates", "community"],
                }
            ),
            encoding="utf-8",
        )

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "governance_sandbox.cli",
                "run",
                "--scenario-file",
                str(scenario_file),
            ],
            cwd=ROOT,
            env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            capture_output=True,
            text=True,
            check=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["scenario"]["name"], "Delegates Roundtable")


if __name__ == "__main__":
    unittest.main()
