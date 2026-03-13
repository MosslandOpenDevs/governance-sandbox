from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioProposalCopyFileAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_proposal_copy_file_alias_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('proposal_copy_file', readme)
        note = (ROOT / 'docs' / 'SCENARIO_PROPOSAL_COPY_FILE_ALIAS_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('proposal_copy_file', note)


if __name__ == '__main__':
    unittest.main()
