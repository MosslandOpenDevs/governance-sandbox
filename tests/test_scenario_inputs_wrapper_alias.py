from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ScenarioInputsWrapperAliasTest(unittest.TestCase):
    def test_run_accepts_top_level_scenario_inputs_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                "\n".join(
                    [
                        "scenario_inputs:",
                        "  proposal: Ship a delegate-ready treasury review checklist with rollback gates.",
                        "  stakeholders:",
                        "    - name: Delegate council",
                        "      preset: delegates",
                        "    - name: Community stewards",
                        "      preset: community",
                        "  report:",
                        "    title: Scenario inputs wrapper memo",
                        "    summary: Wrapper alias proving scenario import plus markdown/html-ready metadata.",
                    ]
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(
                payload["proposal"],
                "Ship a delegate-ready treasury review checklist with rollback gates.",
            )
            self.assertEqual(payload["scenario"]["report_title"], "Scenario inputs wrapper memo")
            self.assertEqual(
                payload["scenario"]["report_summary"],
                "Wrapper alias proving scenario import plus markdown/html-ready metadata.",
            )
            self.assertEqual(len(payload["responses"]), 2)


if __name__ == "__main__":
    unittest.main()
