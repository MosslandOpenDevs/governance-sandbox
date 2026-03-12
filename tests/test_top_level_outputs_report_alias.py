from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_run_supports_top_level_outputs_report_alias_block() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        scenario_path = tmp / "scenario.yaml"
        scenario_path.write_text(
            """proposal:
  title: Publish staged treasury review
  summary: Share the proposal bundle before execution.
stakeholders:
  - name: Delegate council
    preset: delegates
outputs:
  report:
    title: Output report alias
    subtitle: Replayable bundle
    outputs:
      dir: bundles
      basename: alias-brief
      files:
        markdown: files/alias-brief.md
        html: files/alias-brief.html
        json: files/alias-brief.json
""",
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(SRC)},
            capture_output=True,
            text=True,
            check=True,
        )

        payload = json.loads(result.stdout)
        bundle_dir = scenario_path.parent / "bundles"
        files_dir = scenario_path.parent / "files"
        assert payload["scenario"]["report_title"] == "Output report alias"
        assert payload["scenario"]["report_subtitle"] == "Replayable bundle"
        assert payload["report"]["artifacts"]["directory"] == str(bundle_dir.resolve())
        assert payload["report"]["artifacts"]["basename"] == "alias-brief"
        assert payload["report"]["artifacts"]["markdown"] == str((files_dir / "alias-brief.md").resolve())
        assert payload["report"]["artifacts"]["html"] == str((files_dir / "alias-brief.html").resolve())
        assert payload["report"]["artifacts"]["json"] == str((files_dir / "alias-brief.json").resolve())
        assert (files_dir / "alias-brief.md").exists()
        assert (files_dir / "alias-brief.html").exists()
        assert (files_dir / "alias-brief.json").exists()
