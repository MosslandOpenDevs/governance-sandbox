import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_run_supports_scenario_archive_wrapper_with_markdown_report(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario-archive.yaml"
    report_dir = tmp_path / "reports"
    scenario_path.write_text(
        """
scenario_archive:
  proposal: |
    Adopt a staged delegate communication calendar for treasury updates.
  stakeholders:
    - name: DAO operators
      profile: dao
    - name: Active delegates
      preset: delegates
  report:
    title: Scenario archive wrapper memo
    summary: Scenario archive wrapper keeps scenario-file import tied to markdown/html/json report output.
    outputs:
      basename: scenario-archive-demo
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
            "--report-dir",
            str(report_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["scenario"]["report_title"] == "Scenario archive wrapper memo"
    assert payload["scenario"]["report_summary"] == (
        "Scenario archive wrapper keeps scenario-file import tied to markdown/html/json report output."
    )
    assert payload["report"]["artifacts"]["basename"] == "scenario-archive-demo"

    markdown_report = (report_dir / "scenario-archive-demo.md").read_text(encoding="utf-8")
    assert "## Report title\nScenario archive wrapper memo" in markdown_report
    assert "## Report summary\nScenario archive wrapper keeps scenario-file import tied to markdown/html/json report output." in markdown_report
    assert (report_dir / "scenario-archive-demo.html").exists()
    assert (report_dir / "scenario-archive-demo.json").exists()
