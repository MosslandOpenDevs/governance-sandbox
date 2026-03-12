from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProposalCopyMarkdownAliasTests(unittest.TestCase):
    def test_cli_accepts_proposal_copy_markdown_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.json"
            scenario.write_text(json.dumps({
                "proposal": {"title": "Treasury guardrails", "proposal_copy_markdown": "## Budget\n- Cap spend"},
                "stakeholders": [{"name": "Delegate lead", "preset": "delegate"}],
            }), encoding="utf-8")
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            completed = subprocess.run([sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario)], cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertIn("## Budget", payload["proposal"])


if __name__ == "__main__":
    unittest.main()
