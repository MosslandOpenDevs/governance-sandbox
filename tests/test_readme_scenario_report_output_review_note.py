from pathlib import Path


def test_readme_mentions_scenario_report_output_review_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / 'README.md').read_text(encoding='utf-8')
    note = (root / 'docs' / 'SCENARIO_REPORT_OUTPUT_REVIEW_NOTE.md')

    assert 'docs/SCENARIO_REPORT_OUTPUT_REVIEW_NOTE.md' in readme
    assert note.exists()
