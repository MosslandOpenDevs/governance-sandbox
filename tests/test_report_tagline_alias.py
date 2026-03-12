from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


def test_run_supports_report_tagline_alias_for_report_subtitle() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        scenario_path = tmp / 'scenario.yaml'
        scenario_path.write_text(
            '''proposal: Ship the staged contributor grant policy this week.
stakeholders:
  - name: Core delegates
    preset: delegates
report:
  title: Weekly governance brief
  tagline: Fast reviewer handoff for the approval round
''',
            encoding='utf-8',
        )

        result = subprocess.run(
            [
                sys.executable,
                '-m',
                'governance_sandbox.cli',
                'run',
                '--scenario-file',
                str(scenario_path),
            ],
            cwd=ROOT,
            env={**os.environ, 'PYTHONPATH': str(SRC)},
            capture_output=True,
            text=True,
            check=True,
        )

        payload = json.loads(result.stdout)
        assert payload['scenario']['report_title'] == 'Weekly governance brief'
        assert payload['scenario']['report_subtitle'] == 'Fast reviewer handoff for the approval round'
