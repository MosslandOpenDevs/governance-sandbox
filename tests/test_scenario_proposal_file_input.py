from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScenarioProposalFileInputTests(unittest.TestCase):
    def test_run_accepts_relative_proposal_file_inside_scenario(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal_file = tmp / "proposal.md"
            proposal_file.write_text("Adopt quadratic voting for treasury allocations.", encoding="utf-8")
            scenario_file = tmp / "scenario.yaml"
            scenario_file.write_text(
                """
proposal:
  file: proposal.md
stakeholders:
  - Core contributors
  - Token holders
report:
  title: Treasury voting memo
""".strip(),
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
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["proposal"], "Adopt quadratic voting for treasury allocations.")
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
