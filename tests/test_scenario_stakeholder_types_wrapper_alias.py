from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ScenarioStakeholderTypesWrapperAliasTests(unittest.TestCase):
    def test_run_accepts_wrapped_scenario_with_stakeholder_types(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            scenario_path.write_text(
                "\n".join(
                    [
                        "scenario_demo:",
                        "  stakeholder_types:",
                        "    Delegate circle: delegates",
                        "    Community stewards: community",
                        "  scenario:",
                        "    proposal: Ship a phased treasury review dashboard with explicit rollback checkpoints.",
                        "    report:",
                        "      title: Wrapped stakeholder-types memo",
                        "      outputs:",
                        "        report_dir: exports",
                        "        bundle_name: wrapped-stakeholder-types",
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
            self.assertEqual(payload["summary"]["stakeholder_count"], 2)
            self.assertEqual(payload["scenario"]["report_title"], "Wrapped stakeholder-types memo")
            self.assertTrue((Path(tmpdir) / "exports" / "wrapped-stakeholder-types.html").exists())


if __name__ == "__main__":
    unittest.main()
