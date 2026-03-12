from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportValidateSmallSliceNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_validate_small_slice_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_FILE_REPORT_VALIDATE_SMALL_SLICE_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_FILE_REPORT_VALIDATE_SMALL_SLICE_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
