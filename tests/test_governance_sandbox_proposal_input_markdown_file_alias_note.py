from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GovernanceSandboxProposalInputMarkdownFileAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_proposal_input_markdown_file_alias(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("proposal_input_markdown_file", readme)
        self.assertIn("proposal_input_md_file", readme)

    def test_note_mentions_report_bundle_lane(self) -> None:
        note = (ROOT / "docs" / "GOVERNANCE_SANDBOX_PROPOSAL_INPUT_MARKDOWN_FILE_ALIAS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("proposal_input_markdown_file", note)
        self.assertIn("JSON, Markdown, and HTML report artifacts", note)

if __name__ == "__main__":
    unittest.main()
