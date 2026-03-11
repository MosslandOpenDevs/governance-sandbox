from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportResultCardStartTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_result_card_start(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_RESULT_CARD_START.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_RESULT_CARD_START.md").exists())

    def test_note_keeps_lane_small(self) -> None:
        note = (ROOT / "docs" / "SCENARIO_REPORT_RESULT_CARD_START.md").read_text(encoding="utf-8")

        self.assertIn("import one scenario file", note)
        self.assertIn("render one result card", note)
        self.assertIn("verify one report download action", note)


if __name__ == "__main__":
    unittest.main()
