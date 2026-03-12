from pathlib import Path


def test_readme_mentions_scenario_inputs_report_outputs_example() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')
    assert 'examples/scenario-inputs-report-outputs.yaml' in readme
    assert Path('examples/scenario-inputs-report-outputs.yaml').exists()
