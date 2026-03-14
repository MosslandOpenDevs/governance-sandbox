from pathlib import Path


def test_readme_mentions_scenario_journal_wrapper_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / 'README.md').read_text(encoding='utf-8')

    assert 'docs/SCENARIO_JOURNAL_WRAPPER_NOTE.md' in readme
    assert (root / 'docs' / 'SCENARIO_JOURNAL_WRAPPER_NOTE.md').exists()
