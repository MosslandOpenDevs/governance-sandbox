from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_scenario_source_bundle_note() -> None:
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')

    assert 'docs/GOVERNANCE_SANDBOX_SCENARIO_SOURCE_BUNDLE_NOTE.md' in readme
    assert (ROOT / 'docs' / 'GOVERNANCE_SANDBOX_SCENARIO_SOURCE_BUNDLE_NOTE.md').exists()
