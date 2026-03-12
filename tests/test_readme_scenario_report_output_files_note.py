from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTE = ROOT / "docs" / "SCENARIO_REPORT_OUTPUT_FILES_NOTE.md"


class ScenarioReportOutputFilesNoteReadmeTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_output_files_note(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_OUTPUT_FILES_NOTE.md", readme)
        self.assertTrue(NOTE.exists())

    def test_note_keeps_files_mapping_visible(self) -> None:
        note = NOTE.read_text(encoding="utf-8")

        self.assertIn("report.outputs.files", note)
        self.assertIn("files.json", note)
        self.assertIn("files.markdown", note)
        self.assertIn("files.html", note)


if __name__ == "__main__":
    unittest.main()
