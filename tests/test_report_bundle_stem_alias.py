from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class ReportBundleStemAliasTests(unittest.TestCase):
    def test_report_bundle_stem_alias_sets_default_bundle_basename(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario = tmp / "scenario.yaml"
            scenario.write_text(
                """proposal: Ship a treasury dashboard\nstakeholders:\n  - name: Delegates\n    stance: supportive\nreport_bundle_stem: treasury-dashboard-stem\n""",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario),
                    "--report-dir",
                    str(tmp),
                ],
                cwd=root,
                env={**dict(__import__("os").environ), "PYTHONPATH": str(root / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            artifacts = payload["report"]["artifacts"]
            self.assertTrue(artifacts["markdown"].endswith("treasury-dashboard-stem.md"))
            self.assertTrue(artifacts["html"].endswith("treasury-dashboard-stem.html"))
            self.assertTrue(artifacts["json"].endswith("treasury-dashboard-stem.json"))


if __name__ == "__main__":
    unittest.main()
