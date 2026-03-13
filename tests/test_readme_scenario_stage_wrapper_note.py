from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioStageWrapperNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_stage_wrapper_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_STAGE_WRAPPER_NOTE.md", readme)

    def test_note_mentions_stage_aliases(self) -> None:
        doc = (ROOT / "docs" / "SCENARIO_STAGE_WRAPPER_NOTE.md").read_text(encoding="utf-8")

        self.assertIn("scenario_stage", doc)
        self.assertIn("scenario_stage_bundle", doc)


if __name__ == "__main__":
    unittest.main()
