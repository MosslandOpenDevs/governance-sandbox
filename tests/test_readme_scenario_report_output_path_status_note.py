from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportOutputPathStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_output_path_status_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_OUTPUT_PATH_STATUS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "GOVERNANCE_SANDBOX_SCENARIO_REPORT_OUTPUT_PATH_STATUS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
