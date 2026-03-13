from pathlib import Path


def test_readme_mentions_scenario_file_report_stage_gate() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/SCENARIO_FILE_REPORT_STAGE_GATE.md" in readme
    assert Path("docs/SCENARIO_FILE_REPORT_STAGE_GATE.md").exists()
