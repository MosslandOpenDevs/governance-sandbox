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


class ProposalBodyAliasTests(unittest.TestCase):
    def test_run_accepts_proposal_body_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                """proposal_body: |
  Roll out a staged delegate briefing pack before the final vote.
stakeholders:
  - name: Delegate council
    preset: delegates
  - name: Core contributors
    preset: contributors
report:
  outputs:
    basename: proposal-body-alias
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
            self.assertEqual(payload["proposal"], "Roll out a staged delegate briefing pack before the final vote.")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "proposal-body-alias")

    def test_readme_mentions_proposal_body_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_PROPOSAL_BODY_ALIAS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "GOVERNANCE_SANDBOX_PROPOSAL_BODY_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
