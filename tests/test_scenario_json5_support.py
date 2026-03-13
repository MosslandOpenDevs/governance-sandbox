from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioJson5SupportTests(unittest.TestCase):
    def test_run_accepts_json5_scenario_file_with_comments(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_path = tmp_path / "scenario.json5"
            report_dir = tmp_path / "reports"
            scenario_path.write_text(
                """{
  // phase-one scenario file support should accept json5 extensions
  "proposal": "Adopt staged treasury automation with delegate rollback checkpoints.",
  "stakeholders": ["dao", "delegates", "community"],
  "report": {
    "title": "JSON5 scenario support memo",
    "basename": "json5-scenario-support"
  }
}
""",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
                env={**dict(), **__import__('os').environ, 'PYTHONPATH': str(ROOT / 'src')},
            )
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["scenario"]["scenario_format"], "json5")
            self.assertEqual(payload["scenario"]["report_title"], "JSON5 scenario support memo")
            self.assertTrue((report_dir / "json5-scenario-support.md").exists())
            self.assertTrue((report_dir / "json5-scenario-support.html").exists())
            self.assertTrue((report_dir / "json5-scenario-support.json").exists())


if __name__ == "__main__":
    unittest.main()
