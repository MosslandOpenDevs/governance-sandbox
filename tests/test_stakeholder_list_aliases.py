from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StakeholderListAliasTests(unittest.TestCase):
    def test_cli_accepts_stakeholder_list_alias_in_scenario_file(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                """
proposal: Launch a governance review sprint.
stakeholder_list:
  - name: Treasury delegates
    trait: delegates
  - name: Community stewards
    persona: community
""".strip()
                + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )

        payload = json.loads(completed.stdout)
        responses = {item["name"]: item for item in payload["responses"]}

        self.assertEqual(responses["Treasury delegates"]["preset"], "delegates")
        self.assertEqual(responses["Community stewards"]["preset"], "community")


if __name__ == "__main__":
    unittest.main()
