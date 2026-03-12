from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReportBaseAliasTests(unittest.TestCase):
    def test_report_outputs_base_alias_drives_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            scenario_path.write_text(textwrap.dedent('''\
                proposal: Ship a staged treasury update.
                stakeholders:
                  - Delegates
                report:
                  outputs:
                    base: delegate-review-pack
                    dir: reports
            '''), encoding='utf-8')
            completed = subprocess.run([sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)], cwd=ROOT, text=True, capture_output=True, check=False, env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload['report']['artifacts']['basename'], 'delegate-review-pack')
            self.assertTrue((tmp / 'reports' / 'delegate-review-pack.md').exists())
            self.assertTrue((tmp / 'reports' / 'delegate-review-pack.html').exists())
            self.assertTrue((tmp / 'reports' / 'delegate-review-pack.json').exists())

if __name__ == '__main__':
    unittest.main()
