from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportSlugAliasTests(unittest.TestCase):
    def test_run_supports_report_slug_alias_for_report_dir_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scenario_path = root / "scenario.yaml"
            report_dir = root / "artifacts"
            scenario_path.write_text(
                """
proposal: Ship a phased treasury automation pilot.
stakeholders:
  - name: DAO stewards
    preset: dao
  - name: Treasury delegates
    preset: delegates
report:
  title: Treasury automation memo
  slug: delegate-review-pack
""".strip()
                + "\n",
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
                    str(report_dir),
                ],
                cwd=Path(__file__).resolve().parents[1],
                env={**__import__("os").environ, "PYTHONPATH": "src"},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            artifacts = payload["report"]["artifacts"]
            self.assertTrue(artifacts["json"].endswith("delegate-review-pack.json"))
            self.assertTrue(artifacts["markdown"].endswith("delegate-review-pack.md"))
            self.assertTrue(artifacts["html"].endswith("delegate-review-pack.html"))


if __name__ == "__main__":
    unittest.main()
