from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestScenarioSessionBundleWrapper(unittest.TestCase):
    def test_scenario_session_bundle_wrapper_generates_named_report_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            report_dir = Path(tmp_dir) / 'artifacts'
            env = os.environ.copy()
            existing_pythonpath = env.get('PYTHONPATH')
            env['PYTHONPATH'] = str(ROOT / 'src') if not existing_pythonpath else f"{ROOT / 'src'}:{existing_pythonpath}"
            completed = subprocess.run(
                [
                    'python3',
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    'examples/scenario-session-bundle.yaml',
                    '--report-dir',
                    str(report_dir),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )

            result = json.loads(completed.stdout)
            self.assertEqual(result['scenario']['scenario_file'], 'workshop/session-bundle.yaml')
            self.assertTrue((report_dir / 'session-bundle-memo.json').exists())
            self.assertTrue((report_dir / 'session-bundle-memo.md').exists())
            self.assertTrue((report_dir / 'session-bundle-memo.html').exists())


if __name__ == '__main__':
    unittest.main()
