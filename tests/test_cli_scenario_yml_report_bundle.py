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


class GovernanceSandboxScenarioYmlReportBundleTests(unittest.TestCase):
    def test_yml_scenario_file_writes_json_markdown_and_html_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yml"
            scenario_path.write_text(
                "\n".join(
                    [
                        'proposal: "Ship contributor budget transparency report."',
                        "stakeholders:",
                        '  - name: "DAO delegates"',
                        '    preset: "delegates"',
                        '  - name: "Core contributors"',
                        '    preset: "contributors"',
                        "report:",
                        "  outputs:",
                        '    report_dir: "artifacts"',
                        '    bundle_name: "yml-report-bundle"',
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            report_dir = tmp / "artifacts"
            self.assertEqual(payload["report"]["scenario_format"], "yaml")
            self.assertTrue((report_dir / "yml-report-bundle.json").exists())
            self.assertTrue((report_dir / "yml-report-bundle.md").exists())
            self.assertTrue((report_dir / "yml-report-bundle.html").exists())


if __name__ == "__main__":
    unittest.main()
