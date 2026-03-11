from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTE = ROOT / "docs" / "SCENARIO_REPORT_PATHS_NOTE.md"


class ScenarioReportPathsNoteReadmeTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_paths_note(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_PATHS_NOTE.md", readme)
        self.assertTrue(NOTE.exists())

    def test_scenario_report_paths_note_keeps_artifact_path_scope_visible(self) -> None:
        note = NOTE.read_text(encoding="utf-8")

        self.assertIn("scenario file path", note)
        self.assertIn("report directory path", note)
        self.assertIn("JSON, Markdown, and HTML artifact paths", note)


if __name__ == "__main__":
    unittest.main()
