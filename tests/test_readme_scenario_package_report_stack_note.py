from pathlib import Path
import unittest


class ScenarioPackageReportStackNoteTest(unittest.TestCase):
    def test_note_exists_with_package_and_report_stack_language(self) -> None:
        note = Path("docs/SCENARIO_PACKAGE_REPORT_STACK_NOTE.md")
        self.assertTrue(note.exists())
        text = note.read_text(encoding="utf-8")
        self.assertIn("scenario_package", text)
        self.assertIn("JSON/Markdown/HTML report stack", text)


if __name__ == "__main__":
    unittest.main()
