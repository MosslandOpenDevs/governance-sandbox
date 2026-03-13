from pathlib import Path
import unittest


class ReadmeScenarioStdinReportOwnerNoteTest(unittest.TestCase):
    def test_readme_mentions_scenario_stdin_report_owner_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_SCENARIO_STDIN_REPORT_OWNER_NOTE.md", readme)
        self.assertTrue((root / "docs" / "GOVERNANCE_SANDBOX_SCENARIO_STDIN_REPORT_OWNER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
