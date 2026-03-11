from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReportArtifactBundleStartTests(unittest.TestCase):
    def test_readme_mentions_scenario_report_artifact_bundle_start(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/SCENARIO_REPORT_ARTIFACT_BUNDLE_START.md", readme)
        self.assertTrue((ROOT / "docs" / "SCENARIO_REPORT_ARTIFACT_BUNDLE_START.md").exists())


if __name__ == "__main__":
    unittest.main()
