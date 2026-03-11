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


class GovernanceSandboxReportStemAliasTests(unittest.TestCase):
    def test_report_dir_supports_nested_report_stem_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """proposal: Publish a staged delegate memo before execution.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  title: Delegate memo
  stem: delegate-memo-pack
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "delegate-memo-pack")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-memo-pack")
            self.assertTrue((report_dir / "delegate-memo-pack.md").exists())
            self.assertTrue((report_dir / "delegate-memo-pack.html").exists())
            self.assertTrue((report_dir / "delegate-memo-pack.json").exists())

    def test_report_dir_supports_top_level_report_stem_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Stage a community review memo before activation.",
                        "stakeholders": [{"name": "Community stewards", "preset": "community"}],
                        "report_stem": "community-review-pack",
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_basename"], "community-review-pack")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "community-review-pack")
            self.assertTrue((report_dir / "community-review-pack.md").exists())
            self.assertTrue((report_dir / "community-review-pack.html").exists())
            self.assertTrue((report_dir / "community-review-pack.json").exists())


if __name__ == "__main__":
    unittest.main()
