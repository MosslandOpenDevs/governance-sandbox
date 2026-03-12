from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_accepts_faction_and_bloc_aliases_in_scenario_map(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.yaml"
    scenario_path.write_text(
        """
proposal: Rebalance treasury reporting into a delegate-ready review lane.
stakeholders:
  treasury_stewards:
    faction: Treasury stewards
    bloc: delegates
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
    response = payload["responses"][0]

    assert response["name"] == "Treasury stewards"
    assert response["preset"] == "delegates"
