from pathlib import Path


def test_readme_mentions_scenario_file_report_json_yaml_priority_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / 'README.md').read_text(encoding='utf-8')

    assert 'docs/SCENARIO_FILE_REPORT_JSON_YAML_PRIORITY_NOTE.md' in readme
    assert (root / 'docs' / 'SCENARIO_FILE_REPORT_JSON_YAML_PRIORITY_NOTE.md').exists()
