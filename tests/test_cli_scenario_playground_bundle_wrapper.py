from governance_sandbox.cli import _load_scenario


def test_cli_accepts_scenario_playground_bundle_wrapper(tmp_path):
    scenario = tmp_path / "scenario-playground-bundle.yaml"
    scenario.write_text(
        """scenario_playground_bundle:
  proposal:
    title: Treasury checkpoint replay
    summary: Keep scenario file inputs lightweight and reusable.
  stakeholders:
    - dao
    - delegates
  report:
    title: Playground bundle report
""",
        encoding="utf-8",
    )

    loaded = _load_scenario(scenario)

    assert loaded["proposal"]["title"] == "Treasury checkpoint replay"
    assert loaded["stakeholders"] == ["dao", "delegates"]
    assert loaded["report"]["title"] == "Playground bundle report"
