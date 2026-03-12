from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GovernanceSandboxCliListPresetsJsonTraitKeysTests(unittest.TestCase):
    def test_list_presets_json_exposes_trait_keys_for_web_demo_forms(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--list-presets-json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["presets"]["dao"]["key"], "dao")
        self.assertEqual(payload["presets"]["delegates"]["key"], "delegates")
        self.assertEqual(payload["presets"]["community"]["key"], "community")


if __name__ == "__main__":
    unittest.main()
