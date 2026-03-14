import json
import subprocess
import sys
from pathlib import Path
import textwrap


def test_report_bundle_title_alias_sets_default_bundle_basename(tmp_path: Path) -> None:
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text(textwrap.dedent("""
    proposal: Ship a staged voting sandbox
    stakeholders:
      - name: Delegates
        stance: supportive
    report_bundle_title: Delegate Memo Bundle
    report_dir: exports
    """), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    artifacts = payload["report"]["artifacts"]
    assert artifacts["basename"] == "delegate-memo-bundle"
    assert artifacts["markdown"].endswith("delegate-memo-bundle.md")
    assert artifacts["html"].endswith("delegate-memo-bundle.html")
