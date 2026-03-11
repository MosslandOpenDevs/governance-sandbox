from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.cli import _render_html_report


class HtmlReportScenarioPanelTests(unittest.TestCase):
    def test_html_report_shows_report_metadata_without_name_or_context(self) -> None:
        report = _render_html_report({
            "proposal": "Ship a staged governance change.",
            "recommendation": "Proceed with revision",
            "responses": [],
            "major_risks": [],
            "decision_memo": "Keep the memo short.",
            "scenario": {
                "report_title": "Delegate-ready memo",
                "report_summary": "Short summary",
                "report_audience": "delegates, contributors",
                "tags": ["governance", "treasury"],
            },
            "summary": {},
            "report": {},
        })

        self.assertIn("Delegate-ready memo", report)
        self.assertIn("Short summary", report)
        self.assertIn("delegates, contributors", report)
        self.assertIn("governance, treasury", report)
        self.assertIn("Scenario tags:", report)


if __name__ == "__main__":
    unittest.main()
