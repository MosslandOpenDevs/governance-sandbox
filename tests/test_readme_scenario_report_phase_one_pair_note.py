from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportPhaseOnePairNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_phase_one_pair_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_REPORT_PHASE_ONE_PAIR_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_REPORT_PHASE_ONE_PAIR_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
