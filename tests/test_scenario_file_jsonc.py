from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioFileJsoncTests(unittest.TestCase):
    def test_cli_accepts_jsonc_scenario_file_with_line_comments(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.jsonc"
            scenario_path.write_text(
                """
// comment
{
  "proposal": "Ship markdown reports for scenario-based governance rehearsals.",
  "stakeholders": ["dao", "community"]
}
""".strip(),
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
                env={"PYTHONPATH": str(ROOT / "src")},
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["report"]["scenario_format"], "jsonc")
        self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
