from pathlib import Path


def test_readme_mentions_scenario_report_file_alias_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / 'README.md').read_text(encoding='utf-8')
    note = (root / 'docs' / 'SCENARIO_REPORT_FILE_ALIAS_NOTE.md').read_text(encoding='utf-8')

    assert 'docs/SCENARIO_REPORT_FILE_ALIAS_NOTE.md' in readme
    assert 'scenario-file input' in note
    assert 'report-file aliases' in note
