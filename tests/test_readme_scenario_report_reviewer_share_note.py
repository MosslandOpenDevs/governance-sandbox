from pathlib import Path


def test_readme_mentions_scenario_report_reviewer_share_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docs/SCENARIO_REPORT_REVIEWER_SHARE_NOTE.md" in readme
    assert "full markdown/html/json bundle" in readme
