from pathlib import Path


def test_readme_scenario_lab_bundle_wrapper_line() -> None:
    text = Path('README.md').read_text(encoding='utf-8')

    assert 'scenario_lab_bundle' in text
    assert 'markdown/html/json report bundle' in text
