from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_cli_accepts_direct_proposal_file_alias(tmp_path: Path) -> None:
    proposal_path = tmp_path / "proposal.md"
    proposal_path.write_text("# Treasury Refresh\n\nShip the markdown report lane first.", encoding="utf-8")
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(
        json.dumps(
            {
                "proposal_file": proposal_path.name,
                "stakeholders": ["delegates", "community"],
            }
        ),
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
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert "Treasury Refresh" in payload["proposal"]
    assert payload["responses"][0]["preset"] == "delegates"
