from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportDirHandoffNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_dir_handoff_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_FILE_REPORT_DIR_HANDOFF_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_FILE_REPORT_DIR_HANDOFF_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
