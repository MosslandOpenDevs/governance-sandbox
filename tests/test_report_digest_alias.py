import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ReportDigestAliasTests(unittest.TestCase):
    def test_run_accepts_report_digest_alias_for_markdown_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario = Path(tmpdir) / "scenario.yaml"
            scenario.write_text(
                """
proposal: Ship scenario-file import and markdown/html reports first.
stakeholders:
  - dao
  - delegates
report:
  title: Digest alias report
  digest: Digest alias for markdown/html/json bundle output.
""".strip(),
                encoding="utf-8",
            )
            report_dir = Path(tmpdir) / "reports"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario),
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(__import__("os").environ), "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_summary"], "Digest alias for markdown/html/json bundle output.")
            markdown = (report_dir / "digest-alias-report.md").read_text(encoding="utf-8")
            self.assertIn("Digest alias for markdown/html/json bundle output.", markdown)


if __name__ == "__main__":
    unittest.main()
