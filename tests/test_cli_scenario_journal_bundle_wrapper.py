from governance_sandbox.cli import _load_scenario


def test_cli_accepts_scenario_journal_bundle_wrapper(tmp_path):
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text(
        """
scenario_journal_bundle:
  proposal:
    title: Delegate journal import
    summary: Replay a journal-exported scenario file into the report bundle.
  stakeholders:
    - dao
    - delegates
  report:
    title: Journal replay memo
""".strip(),
        encoding="utf-8",
    )

    loaded = _load_scenario(scenario)

    assert loaded["proposal"]["title"] == "Delegate journal import"
    assert loaded["stakeholders"] == ["dao", "delegates"]
    assert loaded["report"]["title"] == "Journal replay memo"
