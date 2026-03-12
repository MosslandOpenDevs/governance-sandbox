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


class ScenarioTraitMapAliasTests(unittest.TestCase):
    def test_run_accepts_stakeholder_trait_map_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Keep the treasury communications upgrade on schedule.
stakeholder_trait_map:
  Delegate council: delegates
  Builder guild: contributors
report:
  outputs:
    bundle_name: trait-map-aliases
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
            self.assertEqual(payload["report"]["artifacts"]["basename"], "trait-map-aliases")
            self.assertEqual([item["preset"] for item in payload["responses"]], ["delegates", "contributors"])


if __name__ == "__main__":
    unittest.main()
