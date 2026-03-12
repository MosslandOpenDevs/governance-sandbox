from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, '-m', 'governance_sandbox.cli', 'run']


class ReportOutputSlugAliasTests(unittest.TestCase):
    def test_report_output_slug_alias_sets_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.json'
            report_dir = Path(tmpdir) / 'reports'
            scenario_path.write_text(
                json.dumps(
                    {
                        'proposal': 'Ship a staged treasury automation pilot with rollback checkpoints.',
                        'stakeholders': ['dao', 'delegates'],
                        'report': {'output_slug': 'delegate-brief'},
                    }
                ),
                encoding='utf-8',
            )

            subprocess.run(
                [*CLI, '--scenario-file', str(scenario_path), '--report-dir', str(report_dir)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertTrue((report_dir / 'delegate-brief.json').exists())
            self.assertTrue((report_dir / 'delegate-brief.md').exists())
            self.assertTrue((report_dir / 'delegate-brief.html').exists())

    def test_report_outputs_output_slug_alias_sets_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / 'scenario.yaml'
            report_dir = Path(tmpdir) / 'reports'
            scenario_path.write_text(
                '\n'.join([
                    'proposal: Keep the grant budget steady while adding a 60-day growth experiment.',
                    'stakeholders: dao,delegates,community',
                    'report:',
                    '  outputs:',
                    '    output_slug: community-rollout',
                ]),
                encoding='utf-8',
            )

            subprocess.run(
                [*CLI, '--scenario-file', str(scenario_path), '--report-dir', str(report_dir)],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertTrue((report_dir / 'community-rollout.json').exists())
            self.assertTrue((report_dir / 'community-rollout.md').exists())
            self.assertTrue((report_dir / 'community-rollout.html').exists())


if __name__ == '__main__':
    unittest.main()
