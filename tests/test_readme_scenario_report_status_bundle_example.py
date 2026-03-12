from pathlib import Path
import unittest


class ReadmeScenarioReportStatusBundleExampleTest(unittest.TestCase):
    def test_example_exists_with_report_bundle_fields(self) -> None:
        example = Path("examples/scenario-report-status-bundle.yaml")
        self.assertTrue(example.exists())
        text = example.read_text(encoding="utf-8")
        self.assertIn("output_name", text)
        self.assertIn("owner", text)
        self.assertIn("audience", text)


if __name__ == "__main__":
    unittest.main()
