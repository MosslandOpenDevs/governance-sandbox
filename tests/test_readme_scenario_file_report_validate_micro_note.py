from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportValidateMicroNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        note = ROOT / "docs" / "GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_VALIDATE_MICRO_NOTE.md"

        self.assertIn("docs/GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_VALIDATE_MICRO_NOTE.md", readme)
        self.assertTrue(note.exists())


if __name__ == "__main__":
    unittest.main()
