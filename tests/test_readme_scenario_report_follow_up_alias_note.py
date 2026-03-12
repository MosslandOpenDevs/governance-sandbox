from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportFollowUpAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_follow_up_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_FOLLOW_UP_ALIAS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_FOLLOW_UP_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
