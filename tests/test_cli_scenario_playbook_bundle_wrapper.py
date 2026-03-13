import tempfile
import unittest
from pathlib import Path

from governance_sandbox.cli import _load_scenario


class CliScenarioPlaybookBundleWrapperTests(unittest.TestCase):
    def test_cli_accepts_scenario_playbook_bundle_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.yaml"
            scenario.write_text(
                """
scenario_playbook_bundle:
  proposal:
    title: Playbook bundle replay
    summary: Keep wrapper-based imports aligned with report generation.
  stakeholders:
    - delegates
    - investors
  report:
    title: Playbook bundle memo
""".strip(),
                encoding="utf-8",
            )

            loaded = _load_scenario(scenario)

            self.assertEqual(loaded["proposal"]["title"], "Playbook bundle replay")
            self.assertEqual(loaded["stakeholders"], ["delegates", "investors"])
            self.assertEqual(loaded["report"]["title"], "Playbook bundle memo")


if __name__ == "__main__":
    unittest.main()
