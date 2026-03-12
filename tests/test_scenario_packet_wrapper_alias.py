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


class ScenarioPacketWrapperAliasTests(unittest.TestCase):
    def test_run_supports_scenario_packet_wrapper_with_report_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / 'scenario.yaml'
            report_dir = tmp / 'artifacts'
            scenario_path.write_text(
                '''scenario_packet:
  proposal: Publish a staged treasury automation memo before execution.
  stakeholders:
    - name: Delegate council
      preset: delegates
    - name: Builder guild
      preset: contributors
  report:
    title: Packet wrapper memo
    outputs:
      basename: packet-wrapper-demo
''',
                encoding='utf-8',
            )

            result = subprocess.run(
                [
                    sys.executable,
                    '-m',
                    'governance_sandbox.cli',
                    'run',
                    '--scenario-file',
                    str(scenario_path),
                    '--report-dir',
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload['scenario']['report_title'], 'Packet wrapper memo')
            self.assertEqual(payload['report']['artifacts']['basename'], 'packet-wrapper-demo')
            self.assertTrue((report_dir / 'packet-wrapper-demo.md').exists())
            self.assertTrue((report_dir / 'packet-wrapper-demo.html').exists())
            self.assertTrue((report_dir / 'packet-wrapper-demo.json').exists())


if __name__ == '__main__':
    unittest.main()
