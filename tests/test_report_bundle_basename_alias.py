import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


class TestReportBundleBasenameAlias:
    def test_report_bundle_basename_alias_sets_default_bundle_basename(self) -> None:
        with TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.yaml"
            report_dir = Path(tmpdir) / "artifacts"
            scenario_path.write_text(
                "proposal: Ship a governance portal\nstakeholders:\n  - name: Delegates\n    stance: supportive\nreport_bundle_basename: governance-portal-bundle\n",
                encoding="utf-8",
            )
            result = subprocess.run(
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
                cwd=Path(__file__).resolve().parents[1],
                env={**__import__("os").environ, "PYTHONPATH": "src"},
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            report_paths = payload["report_paths"]
            assert Path(report_paths["json"]).name == "governance-portal-bundle.json"
            assert Path(report_paths["markdown"]).name == "governance-portal-bundle.md"
            assert Path(report_paths["html"]).name == "governance-portal-bundle.html"
