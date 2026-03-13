from pathlib import Path


def test_readme_mentions_scenario_file_report_repo45_status_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/SCENARIO_FILE_REPORT_REPO45_STATUS_NOTE.md" in text
