from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReadmeScenarioFileReportDeliveryLadderNote(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_delivery_ladder_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_FILE_REPORT_DELIVERY_LADDER_NOTE.md", readme)
        self.assertTrue((ROOT / "docs/SCENARIO_FILE_REPORT_DELIVERY_LADDER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
