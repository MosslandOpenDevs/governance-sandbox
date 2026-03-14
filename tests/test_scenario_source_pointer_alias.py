from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioSourcePointerAliasTests(unittest.TestCase):
    def test_source_pointer_alias_flows_into_report_metadata(self) -> None:
        payload = {
            "proposal": "Adopt delegate feedback office hours",
            "stakeholders": ["delegates", "contributors"],
            "source_pointer": "fixtures/delegate-office-hours.yaml",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            report_dir = Path(tmpdir) / "artifacts"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

            report = json.loads(completed.stdout)
            self.assertEqual(report["scenario"]["scenario_file"], "fixtures/delegate-office-hours.yaml")
            self.assertEqual(report["report"]["scenario_file"], "fixtures/delegate-office-hours.yaml")


if __name__ == "__main__":
    unittest.main()
