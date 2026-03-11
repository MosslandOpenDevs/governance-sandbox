from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportStackCheckTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_stack_check(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_STACK_CHECK.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_STACK_CHECK.md").exists())


if __name__ == "__main__":
    unittest.main()
