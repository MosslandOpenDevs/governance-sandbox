from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeGovernanceSandboxScenarioReportWebDemoBridgeTests(unittest.TestCase):
    def test_readme_mentions_governance_sandbox_scenario_report_web_demo_bridge(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_WEB_DEMO_BRIDGE.md', readme)

    def test_note_mentions_scenario_report_bundle_and_checkpoint(self) -> None:
        note = (ROOT / 'docs' / 'GOVERNANCE_SANDBOX_SCENARIO_REPORT_WEB_DEMO_BRIDGE.md').read_text(encoding='utf-8')
        self.assertIn('scenario-file import', note)
        self.assertIn('markdown/html/json report bundle', note)
        self.assertIn('form-to-result-card checkpoint', note)


if __name__ == '__main__':
    unittest.main()
