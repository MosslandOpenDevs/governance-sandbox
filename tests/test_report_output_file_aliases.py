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


class ReportOutputFileAliasesTests(unittest.TestCase):
    def test_run_supports_output_file_aliases_for_json_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a treasury policy update with a clear rollback clause.
stakeholders:
  - name: DAO council
    preset: dao
  - name: Active delegates
    preset: delegates
report:
  title: Output file alias rehearsal
  outputs:
    output_name: alias-proof
    output_json_file: exports/custom/alias-proof.json
    output_markdown_file: exports/custom/alias-proof.md
    output_html_file: exports/custom/alias-proof.html
""",
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
            artifacts = payload["report"]["artifacts"]
            custom_dir = scenario_path.parent / "exports" / "custom"

            self.assertEqual(Path(artifacts["json"]), (custom_dir / "alias-proof.json").resolve())
            self.assertEqual(Path(artifacts["markdown"]), (custom_dir / "alias-proof.md").resolve())
            self.assertEqual(Path(artifacts["html"]), (custom_dir / "alias-proof.html").resolve())
            self.assertTrue((custom_dir / "alias-proof.json").exists())
            self.assertTrue((custom_dir / "alias-proof.md").exists())
            self.assertTrue((custom_dir / "alias-proof.html").exists())


if __name__ == "__main__":
    unittest.main()
