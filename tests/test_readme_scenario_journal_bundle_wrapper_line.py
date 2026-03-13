from pathlib import Path


def test_readme_scenario_journal_bundle_wrapper_line() -> None:
    text = Path('README.md').read_text(encoding='utf-8')

    assert 'scenario_journal_bundle' in text
    assert 'report bundle' in text
