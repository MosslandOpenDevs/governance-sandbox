from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioLabelAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_label_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_LABEL_ALIAS_NOTE.md", readme)
        self.assertIn("scenario_label", readme)


if __name__ == "__main__":
    unittest.main()
