import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportOwnerSummaryNoteTest(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/SCENARIO_FILE_REPORT_OWNER_SUMMARY_NOTE.md", readme)

    def test_note_mentions_scenario_file_and_report_bundle(self) -> None:
        note = (ROOT / "docs" / "SCENARIO_FILE_REPORT_OWNER_SUMMARY_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("JSON or YAML scenario file", note)
        self.assertIn("markdown/html/json report bundle", note)


if __name__ == "__main__":
    unittest.main()
