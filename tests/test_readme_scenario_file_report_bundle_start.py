from pathlib import Path
import unittest


class ReadmeScenarioFileReportBundleStartTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_bundle_start(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_FILE_REPORT_BUNDLE_START.md", readme)
        self.assertIn("generate markdown/html/json outputs", readme)


if __name__ == "__main__":
    unittest.main()
