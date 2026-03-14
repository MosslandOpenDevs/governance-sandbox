from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "governance_sandbox.cli", "run"]


class ReportLocationAliasesTests(unittest.TestCase):
    def test_report_location_aliases_write_markdown_and_html_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            markdown_path = tmp / "artifacts" / "location-result.md"
            html_path = tmp / "artifacts" / "location-result.html"
            scenario_path.write_text(json.dumps({
                "proposal": "Load one scenario file and route report artifacts through location aliases.",
                "stakeholders": [{"name": "DAO Council", "preset": "dao"}, {"name": "Delegates", "preset": "delegates"}],
                "report": {
                    "outputs": {
                        "markdown_location": str(markdown_path),
                        "html_location": str(html_path),
                    }
                },
            }), encoding="utf-8")
            completed = subprocess.run(CLI + ["--scenario-file", str(scenario_path)], cwd=ROOT, env={"PYTHONPATH": "src"}, capture_output=True, text=True, check=True)
            payload = json.loads(completed.stdout)
            artifacts = payload["report"]["artifacts"]
            self.assertEqual(Path(artifacts["markdown"]), markdown_path.resolve())
            self.assertEqual(Path(artifacts["html"]), html_path.resolve())
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())


if __name__ == "__main__":
    unittest.main()
