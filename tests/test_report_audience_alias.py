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


class ReportAudienceAliasTests(unittest.TestCase):
    def test_run_supports_top_level_audience_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """name: Audience alias rehearsal
proposal: Stage a contributor review before the final treasury post.
audience:
  - delegates
  - contributors
stakeholders:
  - name: Delegate pod
    preset: delegates
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
                    "--report-markdown",
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_audience"], "delegates, contributors")
            self.assertIn("## Report audience\ndelegates, contributors", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
