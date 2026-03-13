import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / 'README.md').read_text(encoding='utf-8')

class ReadmeScenarioReportPhaseOneRecheckTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_phase_one_recheck(self) -> None:
        self.assertIn('docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_PHASE_ONE_RECHECK.md', README)
        self.assertTrue((ROOT / 'docs' / 'GOVERNANCE_SANDBOX_SCENARIO_REPORT_PHASE_ONE_RECHECK.md').exists())

if __name__ == '__main__':
    unittest.main()
