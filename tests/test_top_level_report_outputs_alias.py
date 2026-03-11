from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


def test_run_supports_top_level_report_outputs_alias_block() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        scenario_path = tmp / 'scenario.yaml'
        scenario_path.write_text(
            '''proposal: Publish the staged treasury memo before execution.
stakeholders:
  - name: Delegate council
    preset: delegates
report_outputs:
  dir: outputs
  basename: delegate-brief
  markdown: outputs/review.md
  html: outputs/review.html
  json: outputs/review.json
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
        assert payload['report']['artifacts']['directory'] == str(outputs_dir.resolve())
        assert payload['report']['artifacts']['basename'] == 'delegate-brief'
        assert payload['report']['artifacts']['markdown'] == str((outputs_dir / 'review.md').resolve())
        assert payload['report']['artifacts']['html'] == str((outputs_dir / 'review.html').resolve())
        assert payload['report']['artifacts']['json'] == str((outputs_dir / 'review.json').resolve())
        assert (outputs_dir / 'review.md').exists()
        assert (outputs_dir / 'review.html').exists()
        assert (outputs_dir / 'review.json').exists()
