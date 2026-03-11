import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioPresetReportStartTest(unittest.TestCase):
    def test_readme_mentions_scenario_preset_report_start(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_PRESET_REPORT_START.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_PRESET_REPORT_START.md").exists())
