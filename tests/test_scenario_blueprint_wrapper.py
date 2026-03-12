from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


class ScenarioBlueprintWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_blueprint_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / 'bundle'
            scenario_path = ROOT / 'examples' / 'scenario-blueprint.yaml'
            result = subprocess.run([sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path), '--report-dir', str(report_dir)], cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(SRC)}, capture_output=True, text=True, check=True)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['scenario']['name'], 'Blueprint rehearsal')
            self.assertEqual(payload['report']['artifacts']['basename'], 'blueprint-rehearsal')
            self.assertTrue((report_dir / 'blueprint-rehearsal.md').exists())
            self.assertTrue((report_dir / 'blueprint-rehearsal.html').exists())
            self.assertTrue((report_dir / 'blueprint-rehearsal.json').exists())

    def test_readme_mentions_scenario_blueprint_wrapper_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/SCENARIO_BLUEPRINT_WRAPPER_NOTE.md', readme)


if __name__ == '__main__':
    unittest.main()
