from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReadmeScenarioReportShortFlagNote(unittest.TestCase):
    def test_readme_mentions_scenario_report_short_flag_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/SCENARIO_REPORT_SHORT_FLAG_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_REPORT_SHORT_FLAG_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
