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


class ProposalInputMarkdownFileAliasTests(unittest.TestCase):
    def test_run_accepts_proposal_input_markdown_file_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal_path = tmp / "proposal.md"
            proposal_path.write_text("# Treasury memo\n\nShip a staged governance report bundle.\n", encoding="utf-8")
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal_input_markdown_file: proposal.md
stakeholders:
  - name: Delegate circle
    preset: delegates
report:
  outputs:
    bundle_name: proposal-input-markdown-file
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
            self.assertIn("Ship a staged governance report bundle.", payload["proposal"])
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "proposal-input-markdown-file")

if __name__ == "__main__":
    unittest.main()
