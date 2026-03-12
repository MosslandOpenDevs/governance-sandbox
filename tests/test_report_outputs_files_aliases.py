from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class GovernanceSandboxReportOutputFilesAliasesTests(unittest.TestCase):
    def test_run_supports_nested_report_output_files_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                textwrap.dedent(
                    """
                    proposal: Publish a delegate-ready treasury automation update.
                    stakeholders:
                      - name: Delegate council
                        preset: delegates
                    report:
                      outputs:
                        basename: delegate-ready
                        files:
                          json: exports/delegate-ready.json
                          markdown: exports/delegate-ready.md
                          html: exports/delegate-ready.html
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            report = payload["report"]["artifacts"]
            self.assertEqual(report["json"], str((tmp / "exports" / "delegate-ready.json").resolve()))
            self.assertEqual(report["markdown"], str((tmp / "exports" / "delegate-ready.md").resolve()))
            self.assertEqual(report["html"], str((tmp / "exports" / "delegate-ready.html").resolve()))
            self.assertTrue((tmp / "exports" / "delegate-ready.json").exists())
            self.assertTrue((tmp / "exports" / "delegate-ready.md").exists())
            self.assertTrue((tmp / "exports" / "delegate-ready.html").exists())


if __name__ == "__main__":
    unittest.main()
