from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliScenarioDemoPackBundleWrapperTests(unittest.TestCase):
    def test_run_accepts_scenario_demo_pack_bundle_wrapper(self) -> None:
        scenario_text = textwrap.dedent(
            """
            scenario_demo_pack_bundle:
              proposal: Add a delegate budget checkpoint before treasury automation ships.
              stakeholders:
                - name: Delegate Council
                  preset: delegates
                - name: Core Contributors
                  preset: contributors
            """
        ).strip()

        with tempfile.TemporaryDirectory() as tmp_dir:
            scenario_path = Path(tmp_dir) / "scenario-demo-pack-bundle.yaml"
            scenario_path.write_text(scenario_text, encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                ],
                cwd=ROOT,
                env={**dict(), "PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertIn("Add a delegate budget checkpoint", completed.stdout)
        self.assertIn("Delegate Council", completed.stdout)
        self.assertIn('"preset": "delegates"', completed.stdout)


if __name__ == "__main__":
    unittest.main()
