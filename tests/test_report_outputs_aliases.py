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


class ReportOutputsAliasesTests(unittest.TestCase):
    def test_run_supports_nested_report_outputs_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a delegate-ready treasury checkpoint before the next vote.
stakeholders:
  - name: DAO council
    preset: dao
  - name: Builder guild
    preset: contributors
report:
  title: Outputs block rehearsal
  outputs:
    directory: exports/bundles
    output_name: outputs-block-demo
    markdown: exports/files/outputs-block-demo.md
    html: exports/files/outputs-block-demo.html
    json: exports/files/outputs-block-demo.json
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
            files_dir = scenario_path.parent / "exports" / "files"
            bundle_dir = scenario_path.parent / "exports" / "bundles"

            self.assertEqual(artifacts["directory"], str(bundle_dir.resolve()))
            self.assertEqual(artifacts["basename"], "outputs-block-demo")
            self.assertEqual(Path(artifacts["json"]), (files_dir / "outputs-block-demo.json").resolve())
            self.assertEqual(Path(artifacts["markdown"]), (files_dir / "outputs-block-demo.md").resolve())
            self.assertEqual(Path(artifacts["html"]), (files_dir / "outputs-block-demo.html").resolve())
            self.assertTrue((files_dir / "outputs-block-demo.json").exists())
            self.assertTrue((files_dir / "outputs-block-demo.md").exists())
            self.assertTrue((files_dir / "outputs-block-demo.html").exists())


if __name__ == "__main__":
    unittest.main()
