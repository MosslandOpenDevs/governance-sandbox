from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeScenarioReportPriorityLadderNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_priority_ladder_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_PRIORITY_LADDER_NOTE.md", readme)
        self.assertTrue((root / "docs" / "SCENARIO_REPORT_PRIORITY_LADDER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
