import unittest
from pathlib import Path


class GovernanceSandboxProposalInputMarkdownPathAliasNoteTest(unittest.TestCase):
    def test_readme_mentions_proposal_input_markdown_path_alias(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')
        self.assertIn('proposal_input_markdown_path', readme)

    def test_note_mentions_proposal_input_markdown_path_aliases(self) -> None:
        root = Path(__file__).resolve().parents[1]
        note = (root / 'docs' / 'GOVERNANCE_SANDBOX_PROPOSAL_INPUT_MARKDOWN_PATH_ALIAS_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('proposal_input_markdown_path', note)
        self.assertIn('proposal_input_md_path', note)


if __name__ == '__main__':
    unittest.main()
