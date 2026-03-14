from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from governance_sandbox.cli import _load_scenario


class ScenarioInputBundleWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_input_bundle_wrapper(self) -> None:
        with TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / 'scenario-input-bundle.yaml'
            scenario.write_text(
                'scenario_input_bundle:\n'
                '  proposal: Shift treasury budget toward growth experiments with rollback guardrails.\n'
                '  stakeholders:\n'
                '    - dao\n'
                '    - delegates\n'
                '    - community\n'
                '  report:\n'
                '    title: Scenario input bundle report\n',
                encoding='utf-8',
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(
                loaded['proposal'],
                'Shift treasury budget toward growth experiments with rollback guardrails.',
            )
            self.assertEqual(loaded['stakeholders'], ['dao', 'delegates', 'community'])
            self.assertEqual(loaded['report']['title'], 'Scenario input bundle report')


if __name__ == '__main__':
    unittest.main()
