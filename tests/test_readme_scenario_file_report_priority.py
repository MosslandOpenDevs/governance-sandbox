from pathlib import Path
import unittest


class ReadmeScenarioFileReportPriorityTest(unittest.TestCase):
    def test_readme_mentions_priority_note(self) -> None:
        readme = Path('README.md').read_text()
        self.assertIn('docs/SCENARIO_FILE_REPORT_PRIORITY.md', readme)


if __name__ == '__main__':
    unittest.main()
