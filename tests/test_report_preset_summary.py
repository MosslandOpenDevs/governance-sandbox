from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.cli import _render_html_report, _render_markdown_report
from governance_sandbox.engine import PRESET_SUMMARIES


class ReportPresetSummaryTests(unittest.TestCase):
    def test_markdown_report_includes_preset_summary_for_known_preset(self) -> None:
        report = _render_markdown_report(
            {
                "proposal": "Stage a treasury checkpoint before rollout.",
                "recommendation": "Proceed with revision",
                "responses": [
                    {
                        "name": "Delegate cohort",
                        "preset": "delegates",
                        "stance": "cautious",
                        "concern": "Needs clearer rollback criteria.",
                        "mitigation": "Add measurable rollback gates.",
                    }
                ],
                "major_risks": ["Narrative drift"],
                "decision_memo": "Tighten the vote memo before launch.",
                "scenario": {},
                "summary": {},
                "report": {},
            }
        )

        self.assertIn(f"- Preset summary: {PRESET_SUMMARIES['delegates']}", report)

    def test_html_report_includes_preset_summary_for_known_preset(self) -> None:
        report = _render_html_report(
            {
                "proposal": "Stage a treasury checkpoint before rollout.",
                "recommendation": "Proceed with revision",
                "responses": [
                    {
                        "name": "DAO council",
                        "preset": "dao",
                        "stance": "cautious",
                        "concern": "Needs scope clarity.",
                        "mitigation": "Clarify roles and reporting cadence.",
                    }
                ],
                "major_risks": ["Narrative drift"],
                "decision_memo": "Tighten the vote memo before launch.",
                "scenario": {},
                "summary": {},
                "report": {},
            }
        )

        self.assertIn("<strong>Preset summary:</strong>", report)
        self.assertIn(PRESET_SUMMARIES["dao"], report)


if __name__ == "__main__":
    unittest.main()
