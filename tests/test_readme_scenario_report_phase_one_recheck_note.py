import unittest
from pathlib import Path


class ReadmeScenarioReportPhaseOneRecheckNoteTests(unittest.TestCase):
    def test_readme_mentions_phase_one_recheck_note(self) -> None:
        text = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_PHASE_ONE_RECHECK_NOTE.md', text)


if __name__ == '__main__':
    unittest.main()
