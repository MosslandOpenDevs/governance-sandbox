from pathlib import Path
import unittest


class ReadmeScenarioReportRelativePathReplayTest(unittest.TestCase):
    def test_readme_mentions_relative_path_replay_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/SCENARIO_REPORT_RELATIVE_PATH_REPLAY.md', readme)


if __name__ == '__main__':
    unittest.main()
