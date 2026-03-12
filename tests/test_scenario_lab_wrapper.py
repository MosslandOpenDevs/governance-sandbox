from governance_sandbox.cli import _load_scenario


def test_scenario_lab_wrapper(tmp_path):
    scenario = tmp_path / "scenario.json"
    scenario.write_text(
        """
{
  "scenario_lab": {
    "proposal": "Launch a delegate education sprint",
    "stakeholders": ["dao", "community"]
  }
}
""".strip(),
        encoding="utf-8",
    )

    loaded = _load_scenario(scenario)

    assert loaded["proposal"] == "Launch a delegate education sprint"
    assert loaded["stakeholders"] == ["dao", "community"]
