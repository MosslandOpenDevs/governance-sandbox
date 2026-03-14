from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_report_output_title_alias_sets_bundle_basename(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.yaml"
    scenario_path.write_text(
        """
proposal: Publish delegate office hours
stakeholders:
  - name: Delegates
    stance: supportive
report_output_title: Delegate Office Hours Memo
""".strip()
        + "\n",
        encoding="utf-8",
    )
    report_dir = tmp_path / "artifacts"

    completed = subprocess.run(
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

    payload = json.loads(completed.stdout)
    assert payload["scenario"]["report_basename"] == "delegate-office-hours-memo"
    assert (report_dir / "delegate-office-hours-memo.json").exists()
    assert (report_dir / "delegate-office-hours-memo.md").exists()
    assert (report_dir / "delegate-office-hours-memo.html").exists()
