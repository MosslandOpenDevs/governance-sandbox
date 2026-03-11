from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from governance_sandbox.cli import _normalize_stakeholders, main


class ScenarioMapObjectAliasesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir_obj = TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)

    def tearDown(self) -> None:
        self.temp_dir_obj.cleanup()

    def test_normalize_stakeholders_accepts_object_aliases(self) -> None:
        stakeholders = _normalize_stakeholders({
            "delegate-slot": {"label": "Lead Delegate", "trait_preset": "delegates"}
        })

        self.assertEqual(stakeholders, [{"name": "Lead Delegate", "preset": "delegates"}])

    def test_run_supports_stakeholder_presets_alias(self) -> None:
        scenario_path = self.temp_dir / "scenario-stakeholder-presets.yaml"
        scenario_path.write_text(
            """
proposal: Launch a DAO tooling sprint for treasury reporting.
stakeholder_presets:
  Treasury Council: delegates
  Builder Guild: contributors
report:
  title: Stakeholder preset alias check
""".strip(),
            encoding="utf-8",
        )

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with patch.object(sys, "argv", [
                "gov-sandbox",
                "run",
                "--scenario-file",
                str(scenario_path),
            ]):
                main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual([response["preset"] for response in payload["responses"]], ["delegates", "contributors"])
        self.assertEqual([response["name"] for response in payload["responses"]], ["Treasury Council", "Builder Guild"])

    def test_run_supports_preset_groups_alias(self) -> None:
        scenario_path = self.temp_dir / "scenario-preset-groups.yaml"
        scenario_path.write_text(
            """
proposal: Adopt a delegated treasury guardrail bundle.
preset_groups:
  Treasury Stewards: delegates
  Core Builders: contributors
report:
  title: Preset groups alias check
""".strip(),
            encoding="utf-8",
        )

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with patch.object(sys, "argv", [
                "gov-sandbox",
                "run",
                "--scenario-file",
                str(scenario_path),
            ]):
                main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual([response["preset"] for response in payload["responses"]], ["delegates", "contributors"])
        self.assertEqual([response["name"] for response in payload["responses"]], ["Treasury Stewards", "Core Builders"])

    def test_run_supports_nested_stakeholder_preset_map_alias(self) -> None:
        scenario_path = self.temp_dir / "scenario-stakeholder-preset-map.yaml"
        scenario_path.write_text(
            """
scenario:
  title: Nested stakeholder preset map alias
  inputs:
    proposal: Ship a staged governance dry run.
    stakeholder_preset_map:
      Delegate Council: delegates
      Community Reviewers: community
""".strip(),
            encoding="utf-8",
        )

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with patch.object(sys, "argv", [
                "gov-sandbox",
                "run",
                "--scenario-file",
                str(scenario_path),
            ]):
                main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual([response["preset"] for response in payload["responses"]], ["delegates", "community"])
        self.assertEqual([response["name"] for response in payload["responses"]], ["Delegate Council", "Community Reviewers"])


if __name__ == "__main__":
    unittest.main()
