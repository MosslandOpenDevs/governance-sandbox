from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProposalInputFileAliasTest(unittest.TestCase):
    def test_proposal_input_file_alias_loads_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal = tmp / "proposal.md"
            proposal.write_text("# Treasury Stream\n\nFund audits and onboarding.", encoding="utf-8")
            scenario = tmp / "scenario.json"
            scenario.write_text(json.dumps({
                "proposal_input_file": str(proposal),
                "stakeholders": ["DAO delegates", "Contributors"],
            }), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
        payload = json.loads(result.stdout)
        self.assertIn("Fund audits and onboarding.", payload["proposal"])


if __name__ == "__main__":
    unittest.main()
