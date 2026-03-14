from pathlib import Path
import unittest


class ReadmeReportBundleStemAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_report_bundle_stem_alias_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/GOVERNANCE_SANDBOX_REPORT_BUNDLE_STEM_ALIAS_NOTE.md", readme)
        note = (root / "docs" / "GOVERNANCE_SANDBOX_REPORT_BUNDLE_STEM_ALIAS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("report_bundle_stem", note)
        self.assertIn("JSON, Markdown, and HTML report bundle", note)


if __name__ == "__main__":
    unittest.main()
