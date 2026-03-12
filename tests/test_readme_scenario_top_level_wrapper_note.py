import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioTopLevelWrapperNoteTest(unittest.TestCase):
    def test_readme_mentions_scenario_top_level_wrapper_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_TOP_LEVEL_WRAPPER_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_TOP_LEVEL_WRAPPER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
