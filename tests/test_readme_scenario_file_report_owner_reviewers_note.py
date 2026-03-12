from pathlib import Path
import unittest


class ReadmeScenarioFileReportOwnerReviewersNoteTests(unittest.TestCase):
    def test_readme_mentions_owner_reviewers_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_FILE_REPORT_OWNER_REVIEWERS_NOTE.md", readme)
        self.assertTrue((root / "docs" / "SCENARIO_FILE_REPORT_OWNER_REVIEWERS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
