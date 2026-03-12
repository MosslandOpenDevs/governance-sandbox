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


class StakeholderTypeAliasTests(unittest.TestCase):
    def test_scenario_file_accepts_type_and_stakeholder_type_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "outputs" / "type-alias.md"
            html_path = tmp / "outputs" / "type-alias.html"
            scenario_path.write_text(
                """proposal:
  title: Launch the delegate reporting pilot
  summary: Use a scenario file to test preset aliases and report generation.
stakeholders:
  - name: Delegate council
    type: delegates
  - name: Neighborhood contributors
    stakeholder_type: contributors
report:
  outputs:
    basename: type-alias-bundle
    markdown: outputs/type-alias.md
    html: outputs/type-alias.html
""",
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual([item["preset"] for item in payload["responses"]], ["delegates", "contributors"])
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertEqual(payload["report"]["artifacts"]["basename"], "type-alias-bundle")


if __name__ == "__main__":
    unittest.main()
