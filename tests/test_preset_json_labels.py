from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PresetJsonLabelsTests(unittest.TestCase):
    def test_list_presets_json_exposes_title_cased_labels_and_summaries(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--list-presets-json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
            env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["presets"]["dao"]["label"], "Dao")
        self.assertEqual(payload["presets"]["delegates"]["label"], "Delegates")
        self.assertTrue(payload["presets"]["community"]["summary"])


if __name__ == "__main__":
    unittest.main()
