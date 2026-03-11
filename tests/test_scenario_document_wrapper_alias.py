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


class ScenarioDocumentWrapperAliasTests(unittest.TestCase):
    def test_run_supports_scenario_document_wrapper_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.json'
            scenario_path.write_text(
                json.dumps(
                    {
                        'scenario_document': {
                            'name': 'Scenario document wrapper rehearsal',
                            'proposal': 'Publish the treasury automation report bundle before execution.',
                            'stakeholders': [
                                {'name': 'Delegate council', 'preset': 'delegates'},
                                {'name': 'Core builders', 'preset': 'contributors'},
                            ],
                            'report': {
                                'title': 'Scenario document wrapper memo',
                                'summary': 'Scenario document wrapper proving scenario-file import plus markdown/html/json report output.'
                            }
                        }
                    }
                ),
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
            self.assertEqual(payload['scenario']['name'], 'Scenario document wrapper rehearsal')
            self.assertEqual(payload['scenario']['report_title'], 'Scenario document wrapper memo')
            self.assertEqual(payload['scenario']['report_summary'], 'Scenario document wrapper proving scenario-file import plus markdown/html/json report output.')
            self.assertEqual([response['preset'] for response in payload['responses']], ['delegates', 'contributors'])
