from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


def test_run_supports_scenario_case_wrapper_alias() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        scenario_path = tmp / 'scenario.yaml'
        scenario_path.write_text(
            '''scenario_case:
  proposal:
    title: Treasury automation pilot
    summary: Stage a DAO rehearsal for pre-vote review.
    bullets:
      - Add a 30 day pilot window
      - Publish an operator rollback checklist
  stakeholders:
    Delegate council: delegates
    Core contributors: contributors
  report:
    title: Treasury automation pilot memo
    outputs:
      dir: outputs
      basename: treasury-automation-pilot
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
        outputs_dir = scenario_path.parent / 'outputs'
        assert payload['scenario']['report_title'] == 'Treasury automation pilot memo'
        assert payload['report']['artifacts']['directory'] == str(outputs_dir.resolve())
        assert payload['report']['artifacts']['basename'] == 'treasury-automation-pilot'
        assert (outputs_dir / 'treasury-automation-pilot.md').exists()
        assert (outputs_dir / 'treasury-automation-pilot.html').exists()
        assert (outputs_dir / 'treasury-automation-pilot.json').exists()
