from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportOutputsArtifactsAliasTests(unittest.TestCase):
    def test_scenario_report_outputs_artifacts_alias_writes_bundle_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario = tmp / "scenario.yaml"
            scenario.write_text(
                """proposal: Launch a delegate digest
stakeholders:
  - delegates
  - community
report:
  outputs:
    basename: digest-round
    artifacts:
      json: outputs/digest-round.json
      markdown: outputs/digest-round.md
      html: outputs/digest-round.html
""",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            artifacts = payload["report"]["artifacts"]
            self.assertTrue((tmp / "outputs" / "digest-round.json").exists())
            self.assertTrue((tmp / "outputs" / "digest-round.md").exists())
            self.assertTrue((tmp / "outputs" / "digest-round.html").exists())
            self.assertTrue(artifacts["json"].endswith("outputs/digest-round.json"))
            self.assertTrue(artifacts["markdown"].endswith("outputs/digest-round.md"))
            self.assertTrue(artifacts["html"].endswith("outputs/digest-round.html"))


if __name__ == "__main__":
    unittest.main()
