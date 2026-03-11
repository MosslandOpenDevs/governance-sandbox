from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_accepts_trait_and_persona_aliases_in_scenario_map(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.yaml"
    scenario_path.write_text(
        """
proposal: Launch a delegate communication sprint.
stakeholders:
  Treasury delegates:
    trait: delegates
  Community stewards:
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

    assert responses["Treasury delegates"]["preset"] == "delegates"
    assert responses["Community stewards"]["preset"] == "community"
