import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class CliScenarioDemoPackWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_demo_pack_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.yaml"
            scenario.write_text(
                """
scenario_demo_pack:
  proposal:
    title: Delegate rehearsal bundle
    summary: Validate a demo-pack import path before the browser prototype.
  stakeholders:
    - delegates
    - community
  report:
    title: Demo pack replay memo
""".strip(),
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(loaded["proposal"]["title"], "Delegate rehearsal bundle")
            self.assertEqual(loaded["stakeholders"], ["delegates", "community"])
            self.assertEqual(loaded["report"]["title"], "Demo pack replay memo")

if __name__ == "__main__":
    unittest.main()
