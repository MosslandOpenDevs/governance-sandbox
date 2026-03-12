from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
EXAMPLE = ROOT / "examples" / "scenario-report-output-files.json"


class ScenarioReportOutputFilesExampleTests(unittest.TestCase):
    def test_readme_mentions_output_files_example(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn("examples/scenario-report-output-files.json", readme)
        self.assertTrue(EXAMPLE.exists())

    def test_example_keeps_report_outputs_files_mapping(self) -> None:
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))

        files = payload["report"]["outputs"]["files"]
        self.assertEqual(set(files), {"json", "markdown", "html"})
        self.assertTrue(files["json"].endswith(".json"))
        self.assertTrue(files["markdown"].endswith(".md"))
        self.assertTrue(files["html"].endswith(".html"))


if __name__ == "__main__":
    unittest.main()
