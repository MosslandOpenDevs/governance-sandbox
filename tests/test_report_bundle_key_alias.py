from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportBundleKeyAliasTests(unittest.TestCase):
    def test_report_bundle_key_alias_sets_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                """
proposal: Approve a contributor-led grants squad.
stakeholders:
  - DAO delegates
report_bundle_key: contributor-grants-brief
""".strip(),
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
                    "--report-dir",
                    tmpdir,
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

        payload = json.loads(completed.stdout)
        artifacts = payload["report"]["artifacts"]
        self.assertTrue(artifacts["json"].endswith("contributor-grants-brief.json"))
        self.assertTrue(artifacts["markdown"].endswith("contributor-grants-brief.md"))
        self.assertTrue(artifacts["html"].endswith("contributor-grants-brief.html"))


if __name__ == "__main__":
    unittest.main()
