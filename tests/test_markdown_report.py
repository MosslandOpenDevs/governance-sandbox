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

    def test_markdown_report_includes_preset_mix_summary(self) -> None:
        report = _render_markdown_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "Proceed with revision",
            "responses": [
                {
                    "name": "Delegates",
                    "preset": "delegates",
                    "stance": "cautious",
                    "concern": "Needs more data",
                    "mitigation": "Add a rollback plan",
                },
                {
                    "name": "Community",
                    "preset": "community",
                    "stance": "skeptical",
                    "concern": "Needs more trust",
                    "mitigation": "Add follow-up updates",
                },
                {
                    "name": "More delegates",
                    "preset": "delegates",
                    "stance": "cautious",
                    "concern": "Needs more metrics",
                    "mitigation": "Add milestones",
                },
            ],
            "major_risks": ["Low turnout"],
            "decision_memo": "Pause until turnout assumptions are clearer.",
            "scenario": {},
            "summary": {
                "stakeholder_count": 3,
                "supportive": 0,
                "cautious": 2,
                "mixed": 0,
                "skeptical": 1,
                "recommendation_label": "Proceed with revision",
            },
            "report": {},
        })

        self.assertIn("- Preset mix: community: 1, delegates: 2", report)

    def test_markdown_report_includes_report_owner(self) -> None:
        report = _render_markdown_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "Proceed with revision",
            "responses": [],
            "major_risks": [],
            "decision_memo": "Keep the memo short.",
            "scenario": {"report_owner": "Governance Working Group"},
            "summary": {},
            "report": {},
        })

        self.assertIn("## Report owner\nGovernance Working Group", report)


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

    def test_html_report_escapes_hero_heading_text(self) -> None:
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

        self.assertIn('<h1>&lt;DAO &amp; Delegates&gt;</h1>', report)
        self.assertNotIn('<h1><DAO & Delegates></h1>', report)

    def test_html_report_includes_preset_mix_panel(self) -> None:
        report = _render_html_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "Proceed with revision",
            "responses": [
                {
                    "name": "Delegates",
                    "preset": "delegates",
                    "stance": "cautious",
                    "concern": "Needs more data",
                    "mitigation": "Add a rollback plan",
                },
                {
                    "name": "Community",
                    "preset": "community",
                    "stance": "skeptical",
                    "concern": "Needs more trust",
                    "mitigation": "Add follow-up updates",
                },
            ],
            "major_risks": [],
            "decision_memo": "Keep the memo short.",
            "scenario": {},
            "summary": {
                "stakeholder_count": 2,
                "supportive": 0,
                "cautious": 1,
                "mixed": 0,
                "skeptical": 1,
                "recommendation_label": "Proceed with revision",
            },
            "report": {},
        })

        self.assertIn("<h2>Preset mix</h2>", report)
        self.assertIn("community: 1, delegates: 1", report)

    def test_html_report_includes_report_owner(self) -> None:
        report = _render_html_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "Proceed with revision",
            "responses": [],
            "major_risks": [],
            "decision_memo": "Keep the memo short.",
            "scenario": {"report_owner": "Governance Working Group"},
            "summary": {},
            "report": {},
        })

        self.assertIn("<strong>Report owner:</strong> Governance Working Group", report)


if __name__ == "__main__":
    unittest.main()
