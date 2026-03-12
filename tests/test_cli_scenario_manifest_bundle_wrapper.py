from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_cli_accepts_scenario_manifest_bundle_wrapper(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(
        json.dumps(
            {
                "scenario_manifest_bundle": {
                    "proposal": "Adopt a delegate review window before treasury votes.",
                    "stakeholders": [
                        {"name": "Core delegates", "preset": "delegates"},
                        {"name": "Builders", "preset": "contributors"},
                    ],
                    "report": {
                        "title": "Delegate review window memo",
                        "outputs": {"basename": "delegate-review-window"},
                    },
                }
            }
        ),
        encoding="utf-8",
    )

    report_dir = tmp_path / "reports"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "governance_sandbox.cli",
            "run",
            "--scenario-file",
            str(scenario_path),
            "--report-dir",
            str(report_dir),
        ],
        cwd=Path(__file__).resolve().parents[1],
        env={"PYTHONPATH": "src"},
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["scenario"]["proposal"] == "Adopt a delegate review window before treasury votes."
    assert payload["report"]["artifacts"]["markdown"].endswith("delegate-review-window.md")
