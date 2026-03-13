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


class CliScenarioCasePackWrapperTests(unittest.TestCase):
    def test_run_supports_scenario_case_pack_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "scenario_case_pack": {
                            "proposal": "Keep scenario-file replay small while report bundle proofs stay easy to regenerate.",
                            "stakeholders": {
                                "Delegate council": "delegates",
                                "Treasury contributors": "contributors",
                            },
                            "report": {
                                "title": "Case pack memo",
                                "outputs": {"basename": "case-pack"},
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
        self.assertEqual(payload["proposal"], "Keep scenario-file replay small while report bundle proofs stay easy to regenerate.")
        self.assertEqual(payload["scenario"]["report_title"], "Case pack memo")
        self.assertEqual(payload["report"]["artifacts"]["basename"], "case-pack")


if __name__ == "__main__":
    unittest.main()
