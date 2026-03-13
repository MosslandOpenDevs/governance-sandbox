import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class ScenarioReviewPackWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_review_pack_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario-review-pack.json"
            scenario.write_text(
                '{"scenario_review_pack":{"proposal":"Shift treasury budget toward growth experiments with rollback guardrails.","stakeholders":["dao","delegates","community"],"report":{"title":"Review pack wrapper report"}}}',
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(
                loaded["proposal"],
                "Shift treasury budget toward growth experiments with rollback guardrails.",
            )
            self.assertEqual(loaded["stakeholders"], ["dao", "delegates", "community"])
            self.assertEqual(loaded["report"]["title"], "Review pack wrapper report")


if __name__ == "__main__":
    unittest.main()
