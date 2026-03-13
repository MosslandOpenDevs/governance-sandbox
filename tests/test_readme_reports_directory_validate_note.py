from pathlib import Path
import unittest


class ReadmeReportsDirectoryValidateNoteTests(unittest.TestCase):
    def test_readme_mentions_reports_directory_validate_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/GOVERNANCE_SANDBOX_REPORTS_DIRECTORY_VALIDATE_NOTE.md', readme)
        doc = (root / 'docs' / 'GOVERNANCE_SANDBOX_REPORTS_DIRECTORY_VALIDATE_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('reports_directory', doc)
        self.assertIn('validation rerun', doc)


if __name__ == '__main__':
    unittest.main()
