from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReadmeScenarioReportOutputReviewNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_output_review_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_OUTPUT_REVIEW_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_OUTPUT_REVIEW_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
