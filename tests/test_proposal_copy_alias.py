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


class ProposalCopyAliasTests(unittest.TestCase):
    def test_run_accepts_proposal_copy_alias(self) -> None:
        payload = {
            "proposal": {
                "title": "Treasury review",
                "proposal_copy": "Adopt quarterly treasury review checkpoints."
            },
            "stakeholders": ["delegates"]
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

        result = json.loads(completed.stdout)
        self.assertEqual(result["proposal"], """Treasury review\n\nAdopt quarterly treasury review checkpoints.""")


if __name__ == "__main__":
    unittest.main()
