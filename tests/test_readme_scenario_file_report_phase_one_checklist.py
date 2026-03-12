from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportPhaseOneChecklistTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_phase_one_checklist(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/SCENARIO_FILE_REPORT_PHASE_ONE_CHECKLIST.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_FILE_REPORT_PHASE_ONE_CHECKLIST.md').exists())


if __name__ == '__main__':
    unittest.main()
