import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class CliScenarioRehearsalPackWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_rehearsal_pack_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.yaml"
            scenario.write_text(
                """
scenario_rehearsal_pack:
  proposal:
    title: Rehearsal pack replay
    summary: Keep scenario-file intake flexible while report bundles stay deterministic.
  stakeholders:
    - delegates
    - community
  report:
    title: Rehearsal pack memo
""".strip(),
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(loaded["proposal"]["title"], "Rehearsal pack replay")
            self.assertEqual(loaded["stakeholders"], ["delegates", "community"])
            self.assertEqual(loaded["report"]["title"], "Rehearsal pack memo")


if __name__ == "__main__":
    unittest.main()
