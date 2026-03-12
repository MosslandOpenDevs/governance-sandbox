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


class ScenarioCaseBundleWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_case_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_case_bundle": {
                            "proposal": "Ship the imported scenario bundle before the forum review.",
                            "stakeholders": {
                                "Delegate board": "delegates",
                                "Core builders": "contributors",
                            },
                            "report": {
                                "title": "Scenario case bundle memo",
                                "outputs": {"basename": "scenario-case-bundle"},
                            },
                        }
                    }
                ),
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
        self.assertEqual(payload["proposal"], "Ship the imported scenario bundle before the forum review.")
        self.assertEqual(payload["scenario"]["report_title"], "Scenario case bundle memo")
        self.assertEqual(payload["report"]["artifacts"]["basename"], "scenario-case-bundle")


if __name__ == "__main__":
    unittest.main()
