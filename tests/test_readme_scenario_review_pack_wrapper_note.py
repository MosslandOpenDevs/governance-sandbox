import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / 'README.md').read_text(encoding='utf-8')

class ReadmeScenarioReviewPackWrapperNoteTests(unittest.TestCase):
    def test_readme_mentions_scenario_review_pack_wrapper_note(self) -> None:
        self.assertIn('scenario_review_pack', README)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_REVIEW_PACK_WRAPPER_NOTE.md').exists())

if __name__ == '__main__':
    unittest.main()
