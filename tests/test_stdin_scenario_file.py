from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class StdinScenarioFileTests(unittest.TestCase):
    def test_run_accepts_stdin_yaml_scenario_with_report_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_text = """name: STDIN treasury rehearsal
proposal: Keep the runway conservative while shipping one user-visible improvement.
stakeholders:
  - name: Delegate bloc
    stance: cautious
    influence: 0.8
  - preset: contributors
report:
  title: STDIN treasury rehearsal memo
  output_name: stdin-treasury-rehearsal
"""
            env = dict(__import__("os").environ)
            env["PYTHONPATH"] = str(SRC) + (__import__("os").pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    "-",
                    "--report-dir",
                    str(report_dir),
                ],
                input=scenario_text,
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "STDIN treasury rehearsal")
            self.assertEqual(payload["report"]["scenario_file"], "stdin")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "stdin-treasury-rehearsal")
            self.assertTrue((report_dir / "stdin-treasury-rehearsal.md").exists())
            self.assertTrue((report_dir / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
