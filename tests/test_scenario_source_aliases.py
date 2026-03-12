from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestScenarioSourceAliases(unittest.TestCase):
    def test_run_prefers_scenario_source_aliases_for_stdin_replays(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            markdown_path = Path(tmp_dir) / "report.md"
            html_path = Path(tmp_dir) / "report.html"
            payload = {
                "scenario_source": "fixtures/treasury-upgrade.yaml",
                "proposal": "Ship the treasury automation rollout with a staged fallback plan.",
                "stakeholders": [
                    {"name": "Delegates", "traits": ["governance", "risk-aware"]},
                    {"name": "Contributors", "traits": ["delivery", "execution"]},
                ],
                "report": {"title": "Treasury automation memo"},
            }

            env = os.environ.copy()
            existing_pythonpath = env.get("PYTHONPATH")
            env["PYTHONPATH"] = str(ROOT / "src") if not existing_pythonpath else f"{ROOT / 'src'}:{existing_pythonpath}"
            completed = subprocess.run(
                [
                    "python3",
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    "-",
                    "--report-markdown",
                    str(markdown_path),
                    "--report-html",
                    str(html_path),
                ],
                cwd=ROOT,
                env=env,
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                check=True,
            )

            result = json.loads(completed.stdout)
            self.assertEqual(result["scenario"]["scenario_file"], "fixtures/treasury-upgrade.yaml")
            self.assertEqual(result["report"]["scenario_file"], "fixtures/treasury-upgrade.yaml")
            self.assertIn("## Scenario source\nfixtures/treasury-upgrade.yaml", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("<strong>Scenario source:</strong> fixtures/treasury-upgrade.yaml", html_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
