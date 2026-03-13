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


class CliInputsReportBundleExampleTests(unittest.TestCase):
    def test_inputs_report_bundle_example_writes_json_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source = ROOT / "examples" / "scenario-inputs-report-bundle.json"
            scenario_path = tmp / source.name
            scenario_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            report_dir = tmp / "artifacts" / "inputs-bundle"
            self.assertEqual(payload["scenario"]["name"], "Delegate transparency rehearsal")
            self.assertTrue((report_dir / "report.json").exists())
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
