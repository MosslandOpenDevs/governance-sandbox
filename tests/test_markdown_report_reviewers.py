from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.cli import _render_html_report, _render_markdown_report


class ReportReviewersTests(unittest.TestCase):
    def test_markdown_report_includes_report_reviewers(self) -> None:
        report = _render_markdown_report({
            'proposal': 'Ship a staged governance change.',
            'recommendation': 'Proceed with revision',
            'responses': [],
            'major_risks': [],
            'decision_memo': 'Keep the memo short.',
            'scenario': {'report_reviewers': 'Ops Council, Delegate Leads'},
            'summary': {},
            'report': {},
        })

        self.assertIn('## Report reviewers\nOps Council, Delegate Leads', report)

    def test_html_report_includes_report_reviewers(self) -> None:
        report = _render_html_report({
            'proposal': 'Ship a staged governance change.',
            'recommendation': 'Proceed with revision',
            'responses': [],
            'major_risks': [],
            'decision_memo': 'Keep the memo short.',
            'scenario': {'report_reviewers': 'Ops Council, Delegate Leads'},
            'summary': {},
            'report': {},
        })

        self.assertIn('<strong>Report reviewers:</strong> Ops Council, Delegate Leads', report)


if __name__ == '__main__':
    unittest.main()
