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

from governance_sandbox.cli import _render_html_report, _render_markdown_report


class ScenarioFormatMetadataTests(unittest.TestCase):
    def test_markdown_report_includes_scenario_format(self) -> None:
        report = _render_markdown_report({
            'proposal': 'Ship a staged governance change.',
            'recommendation': 'Proceed with revision',
            'responses': [],
            'major_risks': [],
            'decision_memo': 'Keep the memo short.',
            'scenario': {'scenario_format': 'yaml'},
            'summary': {},
            'report': {'scenario_format': 'yaml'},
        })

        self.assertIn('## Scenario format\nyaml', report)

    def test_html_report_includes_scenario_format(self) -> None:
        report = _render_html_report({
            'proposal': 'Ship a staged governance change.',
            'recommendation': 'Proceed with revision',
            'responses': [],
            'major_risks': [],
            'decision_memo': 'Keep the memo short.',
            'scenario': {'scenario_format': 'json'},
            'summary': {},
            'report': {'scenario_format': 'json'},
        })

        self.assertIn('<strong>Scenario format:</strong> json', report)

    def test_cli_detects_yaml_scenario_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            scenario_path.write_text(
                'proposal: Ship staged messaging updates.\n'
                'stakeholders:\n'
                '  - name: Delegate council\n'
                '    preset: delegates\n',
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
            self.assertEqual(payload['scenario']['scenario_format'], 'yaml')
            self.assertEqual(payload['report']['scenario_format'], 'yaml')


if __name__ == '__main__':
    unittest.main()
