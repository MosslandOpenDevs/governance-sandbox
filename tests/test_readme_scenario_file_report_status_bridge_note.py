from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportStatusBridgeNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_status_bridge_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        note = (ROOT / 'docs' / 'SCENARIO_FILE_REPORT_STATUS_BRIDGE_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_FILE_REPORT_STATUS_BRIDGE_NOTE.md', readme)
        self.assertIn('scenario file', note)
        self.assertIn('JSON/Markdown/HTML report bundle', note)
        self.assertIn('validation green', note)


if __name__ == '__main__':
    unittest.main()
