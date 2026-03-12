from pathlib import Path
import unittest


class ReadmeScenarioArchiveReportStackNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_archive_report_stack_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/SCENARIO_ARCHIVE_REPORT_STACK_NOTE.md', readme)
        note = root / 'docs' / 'SCENARIO_ARCHIVE_REPORT_STACK_NOTE.md'
        self.assertTrue(note.exists())
        note_text = note.read_text(encoding='utf-8')
        self.assertIn('scenario_archive', note_text)
        self.assertIn('JSON/Markdown/HTML report stack', note_text)


if __name__ == '__main__':
    unittest.main()
