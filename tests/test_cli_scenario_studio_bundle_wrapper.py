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


class CliScenarioStudioBundleWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_studio_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_studio_bundle": {
                            "proposal": "Keep scenario-file inputs and report bundles reusable while the web demo stays small.",
                            "stakeholders": {
                                "Delegate council": "delegates",
                                "Core contributors": "contributors",
                            },
                            "report": {
                                "title": "Studio bundle memo",
                                "outputs": {"basename": "studio-bundle"},
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
        self.assertEqual(payload["proposal"], "Keep scenario-file inputs and report bundles reusable while the web demo stays small.")
        self.assertEqual(payload["scenario"]["report_title"], "Studio bundle memo")
        self.assertEqual(payload["report"]["artifacts"]["basename"], "studio-bundle")


if __name__ == "__main__":
    unittest.main()
