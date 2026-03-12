from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class StakeholderObjectAliasTests(unittest.TestCase):
    def test_run_supports_mapping_style_stakeholders_with_nested_stakeholder_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a delegate-ready treasury checkpoint before voting.
stakeholders:
  reviewer-a:
    stakeholder:
      name: Delegate council
      role: delegates
  reviewer-b:
    participant:
      name: Community forum
      trait: community
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["responses"][0]["name"], "Delegate council")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["name"], "Community forum")
            self.assertEqual(payload["responses"][1]["preset"], "community")


if __name__ == "__main__":
    unittest.main()
