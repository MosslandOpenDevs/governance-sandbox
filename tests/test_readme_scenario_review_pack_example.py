import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeScenarioReviewPackExampleTests(unittest.TestCase):
    def test_readme_mentions_review_pack_example(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/scenario-review-pack.yaml", readme)
        self.assertTrue((ROOT / "examples" / "scenario-review-pack.yaml").exists())


if __name__ == "__main__":
    unittest.main()
