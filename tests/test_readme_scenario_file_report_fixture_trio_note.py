from pathlib import Path
import unittest


class ReadmeScenarioFileReportFixtureTrioNoteTest(unittest.TestCase):
    def test_readme_mentions_fixture_trio_note(self) -> None:
        readme = Path("README.md").read_text()
        self.assertIn("docs/SCENARIO_FILE_REPORT_FIXTURE_TRIO_NOTE.md", readme)

    def test_note_mentions_fixture_and_report_trio(self) -> None:
        note = Path("docs/SCENARIO_FILE_REPORT_FIXTURE_TRIO_NOTE.md").read_text()
        self.assertIn("scenario fixture", note)
        self.assertIn("markdown/html/json report trio", note)


if __name__ == "__main__":
    unittest.main()
