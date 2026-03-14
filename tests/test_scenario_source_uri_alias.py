from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_scenario_source_uri_alias_is_reported(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(json.dumps({
        "proposal": "Ship markdown and html reports",
        "stakeholders": [{"name": "DAO", "stance": "support", "influence": 0.8, "rationale": "Needs reusable reporting."}],
        "scenario_source_uri": "fixtures/phase-one-scenario.json",
    }), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["scenario_file"] == "fixtures/phase-one-scenario.json"
