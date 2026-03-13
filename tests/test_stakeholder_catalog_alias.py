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


class StakeholderCatalogAliasTests(unittest.TestCase):
    def test_scenario_file_accepts_stakeholder_catalog_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.yaml'
            scenario_path.write_text(
                """proposal: Ship a staged delegate tooling budget with rollback checkpoints.
stakeholder_catalog:
  Delegate council: delegates
  Builder guild: contributors
""",
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, '-m', 'governance_sandbox.cli', 'run', '--scenario-file', str(scenario_path)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual([item['preset'] for item in payload['responses']], ['delegates', 'contributors'])
            self.assertEqual(payload['summary']['stakeholder_count'], 2)


if __name__ == '__main__':
    unittest.main()
