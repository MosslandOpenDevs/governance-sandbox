from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioFileReportReplayStatusNoteTest(unittest.TestCase):
    def test_note_exists_with_phase_one_replay_cues(self) -> None:
        note = (ROOT / "docs" / "SCENARIO_FILE_REPORT_REPLAY_STATUS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("load one JSON/YAML scenario file", note)
        self.assertIn("generate one markdown/html/json report bundle", note)
        self.assertIn("widen presets and web demo only after this replay stays green", note)


if __name__ == "__main__":
    unittest.main()
