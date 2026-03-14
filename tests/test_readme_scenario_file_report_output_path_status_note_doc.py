from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportOutputPathStatusNoteDocTest(unittest.TestCase):
    def test_readme_mentions_output_path_status_note_doc(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        note = (ROOT / 'docs' / 'SCENARIO_FILE_REPORT_OUTPUT_PATH_STATUS_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_FILE_REPORT_OUTPUT_PATH_STATUS_NOTE.md', readme)
        self.assertIn('one imported JSON/YAML scenario file', note)
        self.assertIn('one explicit report-output path/status check', note)


if __name__ == '__main__':
    unittest.main()
