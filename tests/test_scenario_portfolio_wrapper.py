import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class ScenarioPortfolioWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_portfolio_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / 'scenario-portfolio.yaml'
            scenario.write_text(
                """scenario_portfolio:
  proposal:
    title: Treasury runway extension
    summary: Extend runway while keeping contributor morale stable.
  stakeholders:
    - dao
    - investors
    - contributors
  report:
    title: Portfolio wrapper report
""",
                encoding='utf-8',
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(loaded['proposal']['title'], 'Treasury runway extension')
            self.assertEqual(loaded['proposal']['summary'], 'Extend runway while keeping contributor morale stable.')
            self.assertEqual(loaded['stakeholders'], ['dao', 'investors', 'contributors'])
            self.assertEqual(loaded['report']['title'], 'Portfolio wrapper report')


if __name__ == '__main__':
    unittest.main()
