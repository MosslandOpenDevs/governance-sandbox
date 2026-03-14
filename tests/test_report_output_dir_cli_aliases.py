from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportOutputDirCliAliasesTest(unittest.TestCase):
    def test_report_output_dir_alias_writes_report_bundle(self) -> None:
        scenario = {
            "proposal": {"title": "Ship budget dashboard", "summary": "Create a tight pilot before full rollout."},
            "stakeholders": {"DAO Ops": "dao", "Delegate Circle": "delegates"},
            "report": {"title": "Budget dashboard review"},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            report_dir = Path(tmpdir) / "bundle"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-output-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout)

            artifacts = payload["report"]["artifacts"]
            self.assertEqual(Path(artifacts["directory"]), report_dir.resolve())
            self.assertTrue((report_dir / f"{artifacts['basename']}.json").exists())
            self.assertTrue((report_dir / f"{artifacts['basename']}.md").exists())
            self.assertTrue((report_dir / f"{artifacts['basename']}.html").exists())


if __name__ == "__main__":
    unittest.main()
