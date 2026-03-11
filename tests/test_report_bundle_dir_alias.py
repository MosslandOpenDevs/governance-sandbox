from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportBundleDirAliasTests(unittest.TestCase):
    def test_run_supports_report_bundle_dir_aliases_inside_scenario_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario:
  name: Bundle-dir alias rehearsal
report:
  bundle_dir: outputs/bundles
  basename: delegate-bundle
inputs:
  proposal: Add staged treasury checkpoints.
  stakeholders:
    - name: Delegate circle
      preset: delegates
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env={**__import__("os").environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            report_dir = scenario_path.parent / "outputs" / "bundles"

            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "delegate-bundle.json").exists())
            self.assertTrue((report_dir / "delegate-bundle.md").exists())
            self.assertTrue((report_dir / "delegate-bundle.html").exists())


if __name__ == "__main__":
    unittest.main()
