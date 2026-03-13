from pathlib import Path


def test_readme_mentions_scenario_file_report_owner_review_route_note() -> None:
    text = Path('README.md').read_text(encoding='utf-8')
    assert 'docs/SCENARIO_FILE_REPORT_OWNER_REVIEW_ROUTE_NOTE.md' in text
