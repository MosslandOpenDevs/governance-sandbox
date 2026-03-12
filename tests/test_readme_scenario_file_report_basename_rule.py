from pathlib import Path
import unittest


class ReadmeScenarioFileReportBasenameRuleTest(unittest.TestCase):
    def test_readme_mentions_report_basename_rule(self) -> None:
        readme = Path('README.md').read_text()
        self.assertIn('docs/SCENARIO_FILE_REPORT_BASENAME_RULE.md', readme)


if __name__ == '__main__':
    unittest.main()
