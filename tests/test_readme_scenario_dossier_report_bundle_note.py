from pathlib import Path


def test_readme_mentions_scenario_dossier_report_bundle_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/SCENARIO_DOSSIER_REPORT_BUNDLE_NOTE.md" in text
