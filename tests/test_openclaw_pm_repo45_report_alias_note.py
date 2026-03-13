from pathlib import Path


def test_readme_mentions_repo45_report_alias_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / 'README.md').read_text(encoding='utf-8')

    assert 'report.output_name' in readme
    assert 'report_file_stem' in readme
    assert 'docs/SCENARIO_REPORT_FILE_ALIAS_NOTE.md' in readme
