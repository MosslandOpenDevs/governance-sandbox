from governance_sandbox.cli import _load_scenario


def test_cli_accepts_scenario_workbench_bundle_wrapper(tmp_path):
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text(
        """
scenario_workbench_bundle:
  proposal:
    title: Treasury forum rehearsal
    summary: Test a workbench-exported scenario bundle before the delegate call.
  stakeholders:
    - dao
    - contributors
  report:
    title: Workbench replay memo
""".strip(),
        encoding="utf-8",
    )

    loaded = _load_scenario(scenario)

    assert loaded["proposal"]["title"] == "Treasury forum rehearsal"
    assert loaded["stakeholders"] == ["dao", "contributors"]
    assert loaded["report"]["title"] == "Workbench replay memo"
