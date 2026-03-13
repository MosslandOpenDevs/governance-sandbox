from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_scenario_file_report_owner_status_note() -> None:
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert 'docs/SCENARIO_FILE_REPORT_OWNER_STATUS_NOTE.md' in readme
    assert (ROOT / 'docs' / 'SCENARIO_FILE_REPORT_OWNER_STATUS_NOTE.md').exists()
