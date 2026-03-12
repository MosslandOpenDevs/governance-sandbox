from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportOutputRootAliasTests(unittest.TestCase):
    def test_scenario_report_output_root_alias_writes_bundle_under_root(self) -> None:
        root = Path(__file__).resolve().parents[1]
        fixture = root / "examples" / "scenario-report-output-root.yaml"

        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = Path(tmpdir)
            scenario = workdir / fixture.name
            scenario.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
                env={**dict(__import__("os").environ), "PYTHONPATH": str(root / "src")},
            )

            payload = json.loads(completed.stdout)
            outputs = payload["report"]["artifacts"]
            self.assertTrue(outputs["json"].endswith("reports/demo-bundle/council-round.json"))
            self.assertTrue(outputs["markdown"].endswith("reports/demo-bundle/council-round.md"))
            self.assertTrue(outputs["html"].endswith("reports/demo-bundle/council-round.html"))
            self.assertTrue((workdir / "reports" / "demo-bundle" / "council-round.md").exists())

    def test_readme_mentions_report_output_root_alias_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_ROOT_ALIAS_NOTE.md", readme)
        self.assertTrue((root / "docs" / "GOVERNANCE_SANDBOX_REPORT_OUTPUT_ROOT_ALIAS_NOTE.md").exists())
