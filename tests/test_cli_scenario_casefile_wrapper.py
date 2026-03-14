from pathlib import Path
import subprocess
import sys


def test_cli_accepts_scenario_casefile_wrapper(tmp_path):
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text("""
scenario_casefile:
  proposal: Launch a delegate onboarding sprint.
  stakeholders:
    - delegates
    - community
""".strip(), encoding="utf-8")
    result = subprocess.run([sys.executable, "-m", "governance_sandbox", "run", "--scenario-file", str(scenario)], capture_output=True, text=True, check=True)
    assert "Launch a delegate onboarding sprint." in result.stdout
