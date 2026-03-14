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


class GovernanceSandboxStakeholderTypesAliasTests(unittest.TestCase):
    def test_scenario_file_accepts_stakeholder_types_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.json'
            scenario_path.write_text(json.dumps({
                'proposal': 'Ship a delegate transparency dashboard.',
                'stakeholder_types': {
                    'DAO delegates': 'delegates',
                    'Community stewards': 'community'
                },
                'report': {
                    'outputs': {
                        'report_dir': 'artifacts',
                        'bundle_name': 'stakeholder-types-alias'
                    }
                }
            }), encoding='utf-8')

            result = subprocess.run([
                sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)
            ], cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(SRC)}, capture_output=True, text=True, check=True)

            payload = json.loads(result.stdout)
            self.assertEqual(payload['summary']['stakeholder_count'], 2)
            self.assertTrue((tmp / 'artifacts' / 'stakeholder-types-alias.md').exists())
            self.assertEqual(payload['report']['scenario_format'], 'json')


if __name__ == '__main__':
    unittest.main()
