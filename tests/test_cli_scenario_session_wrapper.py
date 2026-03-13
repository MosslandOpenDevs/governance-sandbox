from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_run_accepts_scenario_session_wrapper(tmp_path: Path) -> None:
    scenario_path = tmp_path / 'scenario-session.json'
    scenario_path.write_text(json.dumps({
        'scenario_session': {
            'proposal': {'title': 'Treasury runway extension', 'body': 'Extend runway by 6 months.'},
            'stakeholder_presets': ['dao', 'community'],
            'report': {'output_slug': 'session-review'}
        }
    }), encoding='utf-8')

    result = subprocess.run(
        [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=True,
    )

    assert 'Treasury runway extension' in result.stdout
    assert 'session-review' in result.stdout
