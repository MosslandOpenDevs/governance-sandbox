from pathlib import Path
import unittest


class ReadmeScenarioFileReportPhaseOneGateNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_phase_one_gate_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/SCENARIO_FILE_REPORT_PHASE_ONE_GATE_NOTE.md', readme)
        self.assertIn('scenario-file import and markdown/html/json report output as the release gate', readme)


if __name__ == '__main__':
    unittest.main()
