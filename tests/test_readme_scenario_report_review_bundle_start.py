from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportReviewBundleStartTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_review_bundle_start(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_REVIEW_BUNDLE_START.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_REVIEW_BUNDLE_START.md").exists())


if __name__ == "__main__":
    unittest.main()
