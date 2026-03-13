from pathlib import Path
import unittest


class ReadmeScenarioFileReportValidateMicroNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_validate_micro_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_VALIDATE_MICRO_NOTE.md", readme)
        self.assertTrue(Path("docs/GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_VALIDATE_MICRO_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
