from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.cli import _render_html_report, _render_markdown_report


class MarkdownReportTests(unittest.TestCase):
    def test_markdown_report_keeps_recommendation_text_literal(self) -> None:
        report = _render_markdown_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "<Hold>",
            "responses": [
                {
                    "name": "Delegates",
                    "preset": "delegates",
                    "stance": "cautious",
                    "concern": "Needs more data",
                    "mitigation": "Add a rollback plan",
                }
            ],
            "major_risks": ["Low turnout"],
            "decision_memo": "Pause until turnout assumptions are clearer.",
            "scenario": {},
            "summary": {},
            "report": {},
        })

        self.assertIn("## Recommendation\n<Hold>", report)
        self.assertNotIn("&lt;Hold&gt;", report)


from governance_sandbox.cli import _render_html_report


class HtmlReportTests(unittest.TestCase):
    def test_html_report_escapes_title_text(self) -> None:
        report = _render_html_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "Proceed with revision",
            "responses": [],
            "major_risks": [],
            "decision_memo": "Keep the memo short.",
            "scenario": {"report_title": '<DAO & Delegates>'},
            "summary": {},
            "report": {},
        })

        self.assertIn('&lt;DAO &amp; Delegates&gt;', report)
        self.assertNotIn('<title><DAO & Delegates></title>', report)


if __name__ == "__main__":
    unittest.main()
