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


class CliScenarioWorkspaceBundleWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_workspace_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps({
                    "scenario_workspace_bundle": {
                        "proposal": "Generate markdown and html governance reports from reusable scenario files.",
                        "stakeholders": {
                            "Delegate circle": "delegates",
                            "Community council": "community",
                        },
                        "report": {
                            "title": "Workspace bundle memo",
                            "outputs": {"basename": "workspace-bundle"},
                        },
                    }
                }),
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
        self.assertEqual(payload["proposal"], "Generate markdown and html governance reports from reusable scenario files.")
        self.assertEqual(payload["scenario"]["report_title"], "Workspace bundle memo")
        self.assertEqual(payload["report"]["artifacts"]["basename"], "workspace-bundle")


if __name__ == "__main__":
    unittest.main()
