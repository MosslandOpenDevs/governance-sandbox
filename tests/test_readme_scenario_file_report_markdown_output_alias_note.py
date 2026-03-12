from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportMarkdownOutputAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_markdown_output_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_FILE_REPORT_MARKDOWN_OUTPUT_ALIAS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_FILE_REPORT_MARKDOWN_OUTPUT_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
