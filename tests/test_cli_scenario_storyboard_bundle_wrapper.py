from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_run_supports_scenario_storyboard_bundle_wrapper() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        scenario_path = Path(tmpdir) / "scenario.json"
        scenario_path.write_text(
            json.dumps(
                {
                    "scenario_storyboard_bundle": {
                        "proposal": "Keep scenario-file import and report generation ahead of demo polish.",
                        "stakeholders": {
                            "Delegate council": "delegates",
                            "Core contributors": "contributors",
                        },
                        "report": {
                            "title": "Storyboard bundle memo",
                            "outputs": {"basename": "storyboard-bundle"},
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(SRC)},
            capture_output=True,
            text=True,
            check=True,
        )

    payload = json.loads(result.stdout)
    assert payload["proposal"] == "Keep scenario-file import and report generation ahead of demo polish."
    assert payload["scenario"]["report_title"] == "Storyboard bundle memo"
    assert payload["report"]["artifacts"]["basename"] == "storyboard-bundle"
