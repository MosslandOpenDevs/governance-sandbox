import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportOutputCodeAliasTest(unittest.TestCase):
    def test_run_supports_report_output_code_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            report_dir = tmp / "reports"
            scenario_path.write_text(json.dumps({
                "proposal": "Ship reviewer-ready markdown and html governance reports from one scenario file.",
                "stakeholders": [{"name": "Delegates", "stance": "supportive"}],
                "report_output_code": "delegate-memo-pack",
                "report_dir": str(report_dir),
            }), encoding="utf-8")

            completed = subprocess.run([sys.executable, "-m", "governance_sandbox.cli", "run", "--scenario-file", str(scenario_path)], cwd=Path(__file__).resolve().parents[1], check=True, capture_output=True, text=True)
            payload = json.loads(completed.stdout)
            artifacts = payload["report"]["artifacts"]
            self.assertEqual(Path(artifacts["json"]).name, "delegate-memo-pack.json")
            self.assertTrue((report_dir / "delegate-memo-pack.md").exists())
            self.assertTrue((report_dir / "delegate-memo-pack.html").exists())


if __name__ == "__main__":
    unittest.main()
