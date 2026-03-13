from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReadmeScenarioPhaseOneReportStackFixture(unittest.TestCase):
    def test_readme_mentions_phase_one_report_stack_fixture(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        fixture = (ROOT / "examples" / "scenario-phase-one-report-stack.yaml").read_text(encoding="utf-8")

        self.assertIn("examples/scenario-phase-one-report-stack.yaml", readme)
        self.assertIn("preset: dao", fixture)
        self.assertIn("preset: delegates", fixture)
        self.assertIn("preset: contributors", fixture)
        self.assertIn("output_slug: treasury-growth-guardrails", fixture)


if __name__ == "__main__":
    unittest.main()
