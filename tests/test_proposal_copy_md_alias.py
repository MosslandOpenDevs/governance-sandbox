from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProposalCopyMdAliasTests(unittest.TestCase):
    def test_run_supports_proposal_copy_md_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal_copy_md": "# Treasury checkpoint\n\nPublish a staged checkpoint before the next vote.",
                        "stakeholders": ["delegates"],
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            self.assertIn("Treasury checkpoint", payload["proposal"])
            self.assertEqual(payload["responses"][0]["name"], "delegates")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")


if __name__ == "__main__":
    unittest.main()
