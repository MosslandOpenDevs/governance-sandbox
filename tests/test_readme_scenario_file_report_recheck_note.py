import unittest
from pathlib import Path


class ReadmeScenarioFileReportRecheckNoteTest(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_recheck_note(self) -> None:
        text = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("docs/SCENARIO_FILE_REPORT_RECHECK_NOTE.md", text)


if __name__ == "__main__":
    unittest.main()
