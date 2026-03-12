from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeGovernanceSandboxReportOutputFilesShortAliasesNoteTests(unittest.TestCase):
    def test_readme_mentions_governance_sandbox_report_output_files_short_aliases_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_FILES_SHORT_ALIASES_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'GOVERNANCE_SANDBOX_REPORT_OUTPUT_FILES_SHORT_ALIASES_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
