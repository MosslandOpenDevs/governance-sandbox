from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportTargetAliasesTests(unittest.TestCase):
    def test_run_supports_top_level_report_target_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario = tmp / "scenario.json"
            output_dir = tmp / "outputs"
            scenario.write_text(json.dumps({
                "proposal": "Adopt phased delegate review.",
                "stakeholders": ["Delegates", "Contributors"],
                "report_markdown_target": "outputs/delegate-review.md",
                "report_html_target": "outputs/delegate-review.html",
            }), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario)],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            markdown_path = output_dir / "delegate-review.md"
            html_path = output_dir / "delegate-review.html"
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str(markdown_path))
            self.assertEqual(payload["report"]["artifacts"]["html"], str(html_path))
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())


if __name__ == "__main__":
    unittest.main()
