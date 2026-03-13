from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportArtifactsRootAliasTests(unittest.TestCase):
    def test_run_supports_top_level_artifacts_root_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """name: Community checkpoint
context: Verify one compact artifacts_root alias.
proposal: Keep the imported scenario tied to one reusable report bundle.
stakeholders:
  - name: Community stewards
    preset: community
report_name: community-checkpoint-pack
artifacts_root: exports/reports
""",
                encoding="utf-8",
            )

            env = dict(__import__("os").environ)
            env["PYTHONPATH"] = str(ROOT / "src")
            proc = subprocess.run(
                [sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(proc.stdout)
            report_dir = scenario_path.parent / "exports" / "reports"
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertTrue((report_dir / "community-checkpoint-pack.json").exists())
            self.assertTrue((report_dir / "community-checkpoint-pack.md").exists())
            self.assertTrue((report_dir / "community-checkpoint-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
