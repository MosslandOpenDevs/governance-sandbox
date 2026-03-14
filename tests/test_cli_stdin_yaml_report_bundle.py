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


class StdinYamlReportBundleTests(unittest.TestCase):
    def test_run_accepts_stdin_yaml_and_writes_report_bundle(self) -> None:
        scenario = """scenario:
  name: Stdin YAML governance replay
proposal:
  title: Stage delegate budget rollout
  summary: Add rollback checkpoints before each tranche.
stakeholder_map:
  Delegate council: delegates
  Community stewards: community
report:
  basename: stdin-yaml-replay
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    "-",
                    "--report-dir",
                    tmpdir,
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                input=scenario,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Stdin YAML governance replay")
            self.assertEqual(payload["scenario"]["scenario_file"], "stdin")
            self.assertEqual(len(payload["responses"]), 2)
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertTrue((Path(tmpdir) / "stdin-yaml-replay.json").exists())
            self.assertTrue((Path(tmpdir) / "stdin-yaml-replay.md").exists())
            self.assertTrue((Path(tmpdir) / "stdin-yaml-replay.html").exists())


if __name__ == "__main__":
    unittest.main()
