from pathlib import Path
import unittest


class ReadmeScenarioFileReportWebDemoPhaseOneNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_file_report_web_demo_phase_one_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_FILE_REPORT_WEB_DEMO_PHASE_ONE_NOTE.md", readme)
        self.assertTrue((root / "docs" / "SCENARIO_FILE_REPORT_WEB_DEMO_PHASE_ONE_NOTE.md").exists())
