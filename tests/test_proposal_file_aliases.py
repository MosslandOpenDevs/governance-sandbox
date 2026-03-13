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
CLI = [sys.executable, "-m", "governance_sandbox.cli", "run"]


class ProposalFileAliasesTests(unittest.TestCase):
    def test_run_supports_proposal_href_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            proposal_path = tmp / "proposal.md"
            scenario_path = tmp / "scenario.yaml"
            proposal_path.write_text(
                "Ship scenario-file support and report bundles before widening the web demo.",
                encoding="utf-8",
            )
            scenario_path.write_text(
                """proposal_href: proposal.md
stakeholders:
  - name: Delegate set
    preset: delegates
  - name: Builder set
    preset: contributors
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                CLI + ["--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertIn("scenario-file support and report bundles", payload["proposal"])
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
