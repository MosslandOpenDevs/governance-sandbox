from pathlib import Path
import unittest


class ReadmeScenarioFileReportExampleNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_example_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/dao-growth-report-bundle.json", readme)
        self.assertIn("named markdown/html/json report bundle", readme)
        self.assertTrue((root / "examples" / "dao-growth-report-bundle.json").exists())
        self.assertTrue((root / "docs" / "SCENARIO_FILE_REPORT_EXAMPLE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
