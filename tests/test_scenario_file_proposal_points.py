from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ScenarioFileProposalPointsTests(unittest.TestCase):
    def test_top_level_proposal_points_and_sections_build_proposal_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            scenario_path = Path(tmp_dir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal_title": "Treasury automation expansion",
                        "proposal_summary": "Ship a scoped automation pilot.",
                        "proposal_points": ["limit budget", "publish weekly updates"],
                        "proposal_sections": [
                            {
                                "title": "Phase 1",
                                "body": "Run a 30-day pilot.",
                                "points": ["measure ops savings"],
                            }
                        ],
                        "stakeholders": ["dao", "community"],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                capture_output=True,
                check=True,
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                env={"PYTHONPATH": "src"},
            )
        payload = json.loads(result.stdout)
        self.assertIn("Treasury automation expansion", payload["proposal"])
        self.assertIn("Key points:", payload["proposal"])
        self.assertIn("- limit budget", payload["proposal"])
        self.assertIn("Sections:", payload["proposal"])
        self.assertIn("Phase 1", payload["proposal"])


if __name__ == "__main__":
    unittest.main()
