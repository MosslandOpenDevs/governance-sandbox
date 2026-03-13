import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


class ReportLeadAliasTests(unittest.TestCase):
    def test_run_accepts_report_lead_alias_for_report_owner(self) -> None:
        payload = {
            "proposal": "Ship one reviewer-ready markdown/html/json governance bundle.",
            "stakeholders": ["dao"],
            "report": {"report_lead": "Scenario Ops"},
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            markdown_path = Path(tmpdir) / "report.md"
            scenario_path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path), "--report-markdown", str(markdown_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            result = json.loads(completed.stdout)
            self.assertEqual(result["scenario"]["report_owner"], "Scenario Ops")
            report_text = markdown_path.read_text(encoding="utf-8")
            self.assertIn("## Report owner", report_text)
            self.assertIn("Scenario Ops", report_text)

    def test_readme_mentions_report_lead_alias_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/SCENARIO_REPORT_LEAD_ALIAS_NOTE.md", readme)
        self.assertTrue((root / "docs" / "SCENARIO_REPORT_LEAD_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
