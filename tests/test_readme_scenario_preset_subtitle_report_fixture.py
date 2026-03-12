from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReadmeScenarioPresetSubtitleReportFixture(unittest.TestCase):
    def test_readme_mentions_scenario_preset_subtitle_report_fixture(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/scenario-preset-subtitle-report.yaml", readme)
        self.assertTrue((ROOT / "examples" / "scenario-preset-subtitle-report.yaml").exists())


if __name__ == "__main__":
    unittest.main()
