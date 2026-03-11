from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.cli import _render_html_report


class HtmlReportScenarioTagsTests(unittest.TestCase):
    def test_html_report_includes_scenario_tags(self) -> None:
        report = _render_html_report({
            'proposal': 'Ship a staged governance change.',
            'recommendation': 'Proceed with revision',
            'responses': [],
            'major_risks': [],
            'decision_memo': 'Keep the memo short.',
            'scenario': {'tags': ['dao', 'treasury']},
            'summary': {},
            'report': {},
        })

        self.assertIn('<strong>Scenario tags:</strong> dao, treasury', report)


if __name__ == '__main__':
    unittest.main()
