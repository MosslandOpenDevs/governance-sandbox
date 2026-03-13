import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "governance_sandbox.cli", "run"]


class ReportsDirectoryAliasTest(unittest.TestCase):
    def test_run_supports_top_level_reports_directory_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """
proposal: Keep scenario-file support and report generation coupled.
stakeholders:
  - name: Delegates
    preset: delegates
report_bundle_name: phase-one-pack
reports_directory: exports/reviewer-bundle
""".strip() + "\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                CLI + ["--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={"PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(completed.stdout)
            report_dir = scenario_path.parent / "exports" / "reviewer-bundle"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "phase-one-pack.json").exists())
            self.assertTrue((report_dir / "phase-one-pack.md").exists())
            self.assertTrue((report_dir / "phase-one-pack.html").exists())

    def test_readme_mentions_reports_directory_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/SCENARIO_REPORTS_DIRECTORY_ALIAS_NOTE.md", readme)
        self.assertIn("reports_directory", readme)
