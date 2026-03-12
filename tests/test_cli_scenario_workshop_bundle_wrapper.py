from governance_sandbox.cli import _load_scenario


def test_cli_accepts_scenario_workshop_bundle_wrapper(tmp_path):
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text(
        """
scenario_workshop_bundle:
  proposal:
    title: Delegate onboarding budget
    summary: Fund a short delegate onboarding sprint before the next vote.
  stakeholders:
    - dao
    - delegates
  report:
    title: Workshop replay memo
""".strip(),
        encoding="utf-8",
    )

    loaded = _load_scenario(scenario)

    assert loaded["proposal"]["title"] == "Delegate onboarding budget"
    assert loaded["stakeholders"] == ["dao", "delegates"]
    assert loaded["report"]["title"] == "Workshop replay memo"
