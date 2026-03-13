from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


def test_run_supports_reports_dir_alias() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        reports_dir = Path(tmpdir) / 'bundle'
        result = subprocess.run(
            [
                sys.executable, '-m', 'governance_sandbox.cli', 'run',
                '--proposal', 'Ship scenario-file intake before widening the demo surface.',
                '--stakeholders', 'delegates,contributors',
                '--reports-dir', str(reports_dir),
            ],
            cwd=ROOT,
            env={**os.environ, 'PYTHONPATH': str(SRC)},
            capture_output=True,
            text=True,
            check=True,
        )

        payload = json.loads(result.stdout)
        artifacts = payload['report']['artifacts']
        assert artifacts['directory'] == str(reports_dir.resolve())
        assert (reports_dir / 'report.json').exists()
        assert (reports_dir / 'report.md').exists()
        assert (reports_dir / 'report.html').exists()
