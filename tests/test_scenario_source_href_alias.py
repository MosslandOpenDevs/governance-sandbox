from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestScenarioSourceHrefAlias(unittest.TestCase):
    def test_scenario_source_href_alias_flows_into_report_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            markdown_path = Path(tmp_dir) / "report.md"
            html_path = Path(tmp_dir) / "report.html"
            payload = {
                "scenario_href": "fixtures/community-rotation.yaml",
                "proposal": "Pilot contributor rotation for governance office hours.",
                "stakeholders": ["delegates", "community"],
                "report": {"title": "Community rotation memo"},
            }

            env = os.environ.copy()
            existing_pythonpath = env.get("PYTHONPATH")
            env["PYTHONPATH"] = str(ROOT / "src") if not existing_pythonpath else f"{ROOT / 'src'}:{existing_pythonpath}"
            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    "-",
                    "--report-markdown",
                    str(markdown_path),
                    "--report-html",
                    str(html_path),
                ],
                cwd=ROOT,
                env=env,
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                check=True,
            )

            result = json.loads(completed.stdout)
            self.assertEqual(result["scenario"]["scenario_file"], "fixtures/community-rotation.yaml")
            self.assertEqual(result["report"]["scenario_file"], "fixtures/community-rotation.yaml")
            self.assertIn("## Scenario source\nfixtures/community-rotation.yaml", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("<strong>Scenario source:</strong> fixtures/community-rotation.yaml", html_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
