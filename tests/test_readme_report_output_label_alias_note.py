from pathlib import Path
import unittest


class ReadmeReportOutputLabelAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_report_output_label_alias_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_LABEL_ALIAS_NOTE.md", readme)


if __name__ == "__main__":
    unittest.main()
