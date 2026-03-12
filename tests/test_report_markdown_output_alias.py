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


class ReportMarkdownOutputAliasTests(unittest.TestCase):
    def test_run_supports_top_level_report_markdown_output_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            scenario_path = tmp_path / "scenario.yaml"
            report_dir = tmp_path / "reports"
            scenario_path.write_text(
                "\n".join(
                    [
                        "proposal: Publish a delegate-ready treasury review memo before execution.",
                        "stakeholders:",
                        "  - name: Delegate circle",
                        "    preset: delegates",
                        "report_markdown_output: outputs/delegate-memo.md",
                    ]
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
            markdown_path = tmp_path / "outputs" / "delegate-memo.md"

            self.assertEqual(payload["report"]["artifacts"]["markdown"], str(markdown_path.resolve()))
            self.assertTrue(markdown_path.exists())
            self.assertIn("delegate-ready treasury review memo", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
