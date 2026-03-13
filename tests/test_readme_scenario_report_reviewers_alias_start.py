import unittest
from pathlib import Path


class ReadmeScenarioReportReviewersAliasStartTest(unittest.TestCase):
    def test_readme_mentions_scenario_report_reviewers_alias_start(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('examples/scenario-report-reviewers.yaml', readme)


if __name__ == '__main__':
    unittest.main()
