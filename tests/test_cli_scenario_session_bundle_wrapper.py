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


class ScenarioSessionBundleWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_session_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_path = tmp_path / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_session_bundle": {
                            "proposal": "Pilot a contributor council review before major treasury votes.",
                            "stakeholders": [
                                {"name": "Delegate circle", "preset": "delegates"},
                                {"name": "Core contributors", "preset": "contributors"},
                            ],
                            "report": {
                                "title": "Scenario session bundle demo",
                                "outputs": {"basename": "scenario-session-bundle-demo"},
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            report_dir = tmp_path / "reports"
            result = subprocess.run(
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Pilot a contributor council review before major treasury votes.")
            self.assertTrue(payload["report"]["artifacts"]["markdown"].endswith("scenario-session-bundle-demo.md"))


if __name__ == "__main__":
    unittest.main()
