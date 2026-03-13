import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class CliScenarioNotebookWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_notebook_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.yaml"
            scenario.write_text(
                """
scenario_notebook:
  proposal:
    title: Delegate education replay
    summary: Shift 15% of rewards budget into delegate education.
  stakeholders:
    - delegates
    - community
  report:
    title: Notebook wrapper replay memo
""".strip(),
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(loaded["proposal"]["title"], "Delegate education replay")
            self.assertEqual(loaded["stakeholders"], ["delegates", "community"])
            self.assertEqual(loaded["report"]["title"], "Notebook wrapper replay memo")


if __name__ == "__main__":
    unittest.main()
