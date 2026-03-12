from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportOwnerAudienceStartTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_owner_audience_start(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_OWNER_AUDIENCE_START.md', readme)
        self.assertTrue((ROOT / 'docs' / 'GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_OWNER_AUDIENCE_START.md').exists())
