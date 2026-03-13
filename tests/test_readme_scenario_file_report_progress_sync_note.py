from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportProgressSyncNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_progress_sync_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_FILE_REPORT_PROGRESS_SYNC_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_FILE_REPORT_PROGRESS_SYNC_NOTE.md').exists())

    def test_note_mentions_phase_one_inputs_reports_and_demo_shape(self) -> None:
        doc = (ROOT / 'docs' / 'SCENARIO_FILE_REPORT_PROGRESS_SYNC_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('JSON/YAML scenario files', doc)
        self.assertIn('markdown/html report artifacts', doc)
        self.assertIn('one form, one primary action, and one result card', doc)
        self.assertIn('smallest scenario -> report bundle', doc)


if __name__ == '__main__':
    unittest.main()
