from pathlib import Path
import unittest


class ReadmeReportSummaryTitleNoteTest(unittest.TestCase):
    def test_readme_mentions_report_summary_title_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("docs/GOVERNANCE_SANDBOX_REPORT_SUMMARY_TITLE_NOTE.md", readme)

    def test_note_exists_and_mentions_report_summary_title(self) -> None:
        note = Path("docs/GOVERNANCE_SANDBOX_REPORT_SUMMARY_TITLE_NOTE.md")
        self.assertTrue(note.exists())
        content = note.read_text(encoding="utf-8")
        self.assertIn("report.summary_title", content)
        self.assertIn("Markdown", content)
        self.assertIn("HTML", content)


if __name__ == "__main__":
    unittest.main()
