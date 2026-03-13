import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class ScenarioDeckWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_deck_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario-deck.json"
            scenario.write_text(
                '{"scenario_deck":{"proposal":"Adopt a staged grants deck with delegate review checkpoints.","stakeholders":["dao","delegates","contributors"],"report":{"title":"Scenario deck wrapper report"}}}',
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(
                loaded["proposal"],
                "Adopt a staged grants deck with delegate review checkpoints.",
            )
            self.assertEqual(loaded["stakeholders"], ["dao", "delegates", "contributors"])
            self.assertEqual(loaded["report"]["title"], "Scenario deck wrapper report")


if __name__ == "__main__":
    unittest.main()
