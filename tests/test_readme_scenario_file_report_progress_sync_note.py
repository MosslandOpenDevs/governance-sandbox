from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportProgressSyncNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_progress_sync_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_FILE_REPORT_PROGRESS_SYNC_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_FILE_REPORT_PROGRESS_SYNC_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
