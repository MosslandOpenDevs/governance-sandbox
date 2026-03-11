from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportOwnerAudienceHandoffTests(unittest.TestCase):
    def test_readme_links_owner_audience_handoff(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/SCENARIO_REPORT_OWNER_AUDIENCE_HANDOFF.md', readme)
        self.assertTrue((ROOT / 'docs' / 'SCENARIO_REPORT_OWNER_AUDIENCE_HANDOFF.md').exists())

    def test_note_mentions_owner_audience_bundle(self):
        note = (ROOT / 'docs' / 'SCENARIO_REPORT_OWNER_AUDIENCE_HANDOFF.md').read_text(encoding='utf-8').lower()
        self.assertIn('owner', note)
        self.assertIn('audience', note)
        self.assertIn('bundle', note)


if __name__ == '__main__':
    unittest.main()
