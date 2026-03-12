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


class ProposalDescriptionAliasTests(unittest.TestCase):
    def test_run_accepts_proposal_description_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                """proposal:
  title: Treasury communication sprint
  proposal_description: |
    Publish a scenario-file-driven treasury comms plan with a markdown report bundle.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  outputs:
    basename: proposal-description-alias
""",
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
            self.assertIn("Publish a scenario-file-driven treasury comms plan", payload["proposal"])
            self.assertEqual(payload["report"]["artifacts"]["basename"], "proposal-description-alias")


if __name__ == "__main__":
    unittest.main()
