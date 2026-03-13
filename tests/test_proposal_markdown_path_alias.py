from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProposalMarkdownPathAliasTests(unittest.TestCase):
    def test_scenario_file_supports_proposal_markdown_path_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal = tmp / "proposal.md"
            proposal.write_text("# Treasury reallocation\n\nKeep the report bundle grounded in markdown input.", encoding="utf-8")
            scenario = tmp / "scenario.json"
            scenario.write_text(json.dumps({
                "proposal_markdown_path": "proposal.md",
                "stakeholders": ["dao", "delegates"],
            }), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertIn("Treasury reallocation", payload["proposal"])
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
