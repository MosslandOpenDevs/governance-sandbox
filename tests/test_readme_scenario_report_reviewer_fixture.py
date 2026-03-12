from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportReviewerFixtureTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_reviewer_fixture(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/scenario-report-reviewer.yaml", readme)
        self.assertTrue((ROOT / "examples" / "scenario-report-reviewer.yaml").exists())


if __name__ == "__main__":
    unittest.main()
