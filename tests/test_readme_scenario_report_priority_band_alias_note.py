from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportPriorityBandAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_priority_band_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("priority_band", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_PRIORITY_BAND_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
