import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class CliScenarioDemoWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_demo_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.yaml"
            scenario.write_text(
                """
scenario_demo:
  proposal:
    title: Browser demo rehearsal
    summary: Validate the shortest demo wrapper before widening the web flow.
  stakeholders:
    - delegates
    - community
  report:
    title: Demo wrapper replay memo
""".strip(),
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(loaded["proposal"]["title"], "Browser demo rehearsal")
            self.assertEqual(loaded["stakeholders"], ["delegates", "community"])
            self.assertEqual(loaded["report"]["title"], "Demo wrapper replay memo")


if __name__ == "__main__":
    unittest.main()
