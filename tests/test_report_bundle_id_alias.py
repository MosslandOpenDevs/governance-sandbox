from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "governance_sandbox.cli", "run"]


class ReportBundleIdAliasTests(unittest.TestCase):
    def test_report_bundle_id_alias_sets_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            report_dir = Path(tmpdir) / "reports"
            scenario_path.write_text(json.dumps({"proposal": "Pilot delegated review queues.", "stakeholders": ["dao", "delegates"], "report": {"bundle_id": "delegate-lane"}}), encoding="utf-8")

            subprocess.run([*CLI, "--scenario-file", str(scenario_path), "--report-dir", str(report_dir)], cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")}, capture_output=True, text=True, check=True)

            self.assertTrue((report_dir / "delegate-lane.json").exists())
            self.assertTrue((report_dir / "delegate-lane.md").exists())
            self.assertTrue((report_dir / "delegate-lane.html").exists())

    def test_report_outputs_bundle_id_alias_sets_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            report_dir = Path(tmpdir) / "reports"
            scenario_path.write_text("\n".join(["proposal: Extend contributor onboarding with a review squad.", "stakeholders: contributors,community", "report:", "  outputs:", "    bundle_id: contributor-lane"]), encoding="utf-8")

            subprocess.run([*CLI, "--scenario-file", str(scenario_path), "--report-dir", str(report_dir)], cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")}, capture_output=True, text=True, check=True)

            self.assertTrue((report_dir / "contributor-lane.json").exists())
            self.assertTrue((report_dir / "contributor-lane.md").exists())
            self.assertTrue((report_dir / "contributor-lane.html").exists())


if __name__ == "__main__":
    unittest.main()
