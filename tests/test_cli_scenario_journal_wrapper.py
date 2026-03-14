from governance_sandbox.cli import _load_scenario


def test_cli_accepts_scenario_journal_wrapper(tmp_path):
    scenario = tmp_path / 'scenario.yaml'
    scenario.write_text(
        """
scenario_journal:
  proposal:
    title: Journal replay
    summary: Rehearse a journal-exported governance scenario.
  stakeholders:
    - dao
    - community
  report:
    title: Journal wrapper report
""".strip(),
        encoding='utf-8',
    )

    loaded = _load_scenario(scenario)

    assert loaded['proposal']['title'] == 'Journal replay'
    assert loaded['stakeholders'] == ['dao', 'community']
    assert loaded['report']['title'] == 'Journal wrapper report'
