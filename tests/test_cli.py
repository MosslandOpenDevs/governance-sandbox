from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class GovernanceSandboxCliTests(unittest.TestCase):
    def test_run_supports_json_scenario_file_and_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            json_path = tmp / "report.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "name": "Treasury reallocation dry run",
                        "context": "Emergency budget review before the next DAO vote.",
                        "proposal": "Shift part of the treasury budget to community growth experiments.",
                        "stakeholders": [
                            {"name": "DAO council", "preset": "dao"},
                            {"name": "Delegate cohort", "preset": "delegates"},
                        ],
                    }
                ),
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
                    "--report-markdown",
                    str(markdown_path),
                    "--report-html",
                    str(html_path),
                    "--report-json",
                    str(json_path),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Shift part of the treasury budget to community growth experiments.")
            self.assertEqual(payload["scenario"]["name"], "Treasury reallocation dry run")
            self.assertEqual(payload["scenario"]["context"], "Emergency budget review before the next DAO vote.")
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertEqual(payload["report"]["scenario_file"], str(scenario_path.resolve()))
            self.assertRegex(payload["report"]["generated_at"], r"Z$")
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertTrue(json_path.exists())
            markdown_report = markdown_path.read_text(encoding="utf-8")
            html_report = html_path.read_text(encoding="utf-8")
            self.assertIn("# Governance Sandbox Report", markdown_report)
            self.assertIn("## Report metadata", markdown_report)
            self.assertIn(f"- Scenario file: {scenario_path.resolve()}", markdown_report)
            self.assertIn("## Scenario\nTreasury reallocation dry run", markdown_report)
            self.assertIn("## Context\nEmergency budget review before the next DAO vote.", markdown_report)
            self.assertIn("### DAO council (dao)", markdown_report)
            self.assertIn("<title>Governance Sandbox Report</title>", html_report)
            self.assertIn(f"<strong>Scenario file:</strong> {scenario_path.resolve()}", html_report)
            self.assertIn("<strong>Scenario:</strong> Treasury reallocation dry run", html_report)
            self.assertIn("Recommendation: Proceed with revision", html_report)
            self.assertIn("DAO council", html_report)

    def test_run_supports_yaml_scenario_file_and_nested_report_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "artifacts" / "reports" / "report.md"
            html_path = tmp / "artifacts" / "reports" / "report.html"
            json_path = tmp / "artifacts" / "reports" / "report.json"
            scenario_path.write_text(
                """name: Delegate sentiment rehearsal
context: Pre-vote dry run for a treasury policy update.
proposal: Add milestone-based reporting to treasury programs.
stakeholders:
  - name: Delegate circle
    preset: delegates
  - name: Community stewards
    preset: community
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
                    "--report-markdown",
                    str(markdown_path),
                    "--report-html",
                    str(html_path),
                    "--report-json",
                    str(json_path),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Delegate sentiment rehearsal")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertTrue(json_path.exists())
            self.assertIn("Community stewards", markdown_path.read_text(encoding="utf-8"))

    def test_run_supports_stdin_scenario_file_and_labels_report_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            markdown_path = tmp / "report.md"
            scenario_payload = json.dumps(
                {
                    "name": "Stdin scenario",
                    "context": "Dry run piped from another tool.",
                    "proposal": "Add a contributor reporting checklist before treasury payouts.",
                    "stakeholders": [
                        {"name": "Delegate cohort", "preset": "delegates"},
                        {"name": "Builder pod", "preset": "contributors"},
                    ],
                }
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    "-",
                    "--report-markdown",
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                input=scenario_payload,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Stdin scenario")
            self.assertEqual(payload["report"]["scenario_file"], "stdin")
            self.assertIn("- Scenario file: stdin", markdown_path.read_text(encoding="utf-8"))

    def test_run_supports_title_decision_aliases_and_group_based_presets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                json.dumps(
                    {
                        "title": "Delegate trust rehearsal",
                        "decision": "Emergency checkpoint before the forum post.",
                        "proposal": "Add quarterly treasury reporting checkpoints.",
                        "stakeholders": [
                            {"stakeholder": "Investor group", "group": "investors"},
                            {"name": "Community circle", "trait": "community"},
                        ],
                    }
                ),
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
                    "--report-markdown",
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Delegate trust rehearsal")
            self.assertEqual(payload["scenario"]["context"], "Emergency checkpoint before the forum post.")
            self.assertEqual(payload["responses"][0]["name"], "Investor group")
            self.assertEqual(payload["responses"][0]["preset"], "investors")
            self.assertEqual(payload["responses"][1]["preset"], "community")
            self.assertIn("## Context\nEmergency checkpoint before the forum post.", markdown_path.read_text(encoding="utf-8"))

    def test_run_supports_proposal_and_stakeholder_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            json_path = tmp / "report.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "title": "Alias-based import",
                        "summary": "Forum dry run before posting the final proposal.",
                        "proposal_text": "Introduce milestone-based reporting for grants.",
                        "participants": [
                            {"stakeholder": "DAO delegates", "group": "delegates"},
                            {"name": "Community reviewers", "trait": "community"},
                        ],
                    }
                ),
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
                    "--report-json",
                    str(json_path),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Introduce milestone-based reporting for grants.")
            self.assertEqual(payload["scenario"]["name"], "Alias-based import")
            self.assertEqual(payload["scenario"]["context"], "Forum dry run before posting the final proposal.")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "community")
            self.assertTrue(json_path.exists())

    def test_run_report_dir_writes_default_report_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "artifacts" / "bundle"
            scenario_path.write_text(
                """title: Community assurance rehearsal
summary: Dry run before publishing the treasury update.
proposal: Add staged spending checkpoints to the growth budget.
actors:
  - stakeholder: Delegate bench
    group: delegates
  - name: Contributor pod
    trait: contributors
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Community assurance rehearsal")
            self.assertTrue((report_dir / "report.json").exists())
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())
            self.assertIn("Delegate bench", (report_dir / "report.md").read_text(encoding="utf-8"))

    def test_run_supports_nested_scenario_and_inputs_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "artifacts"
            scenario_path.write_text(
                """scenario:
  name: Treasury confidence rehearsal
  decision_context: Pre-forum dry run for a budget reallocation memo.
inputs:
  prompt: Rebalance the treasury toward milestone-based ecosystem spending.
  participants:
    - stakeholder: Delegate table
      group: delegates
    - name: Investor circle
      trait: investors
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Rebalance the treasury toward milestone-based ecosystem spending.")
            self.assertEqual(payload["scenario"]["name"], "Treasury confidence rehearsal")
            self.assertEqual(payload["scenario"]["context"], "Pre-forum dry run for a budget reallocation memo.")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "investors")
            self.assertTrue((report_dir / "report.md").exists())

    def test_run_supports_tags_and_outcome_snapshot_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """scenario:
  name: Community alignment rehearsal
  labels:
    - treasury
    - delegates
inputs:
  proposal: Add milestone-based budget checkpoints before new growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
    - name: Community members
      preset: community
    - name: Investor pod
      preset: investors
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["tags"], ["treasury", "delegates"])
            self.assertEqual(payload["summary"]["stakeholder_count"], 3)
            self.assertEqual(payload["summary"]["supportive"], 1)
            self.assertEqual(payload["summary"]["cautious"], 1)
            self.assertEqual(payload["summary"]["skeptical"], 1)
            markdown_report = (report_dir / "report.md").read_text(encoding="utf-8")
            html_report = (report_dir / "report.html").read_text(encoding="utf-8")
            self.assertIn("## Scenario tags\ntreasury, delegates", markdown_report)
            self.assertIn("## Outcome snapshot", markdown_report)
            self.assertIn("- Stakeholders: 3", markdown_report)
            self.assertIn("- Recommendation: Proceed with revision", markdown_report)
            self.assertIn("<h2>Scenario tags</h2><p>treasury, delegates</p>", html_report)
            self.assertIn("<h2>Outcome snapshot</h2>", html_report)


    def test_run_supports_report_title_metadata_in_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """scenario:
  name: Treasury signal rehearsal
  report_title: Delegate-ready rehearsal memo
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_title"], "Delegate-ready rehearsal memo")
            markdown_report = (report_dir / "report.md").read_text(encoding="utf-8")
            html_report = (report_dir / "report.html").read_text(encoding="utf-8")
            self.assertIn("# Delegate-ready rehearsal memo", markdown_report)
            self.assertIn("## Report title\nDelegate-ready rehearsal memo", markdown_report)
            self.assertIn("<title>Delegate-ready rehearsal memo</title>", html_report)
            self.assertIn("<h1>Delegate-ready rehearsal memo</h1>", html_report)
            self.assertIn("<strong>Report title:</strong> Delegate-ready rehearsal memo", html_report)



    def test_run_supports_report_block_title_tags_and_description_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """scenario:
  name: Delegate report rehearsal
  description: Dry run before a forum memo goes live.
report:
  title: Governance memo for delegates
  tags:
    - forum
    - treasury
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["context"], "Dry run before a forum memo goes live.")
            self.assertEqual(payload["scenario"]["report_title"], "Governance memo for delegates")
            self.assertEqual(payload["scenario"]["tags"], ["forum", "treasury"])
            markdown_report = (report_dir / "report.md").read_text(encoding="utf-8")
            html_report = (report_dir / "report.html").read_text(encoding="utf-8")
            self.assertIn("# Governance memo for delegates", markdown_report)
            self.assertIn("## Context\nDry run before a forum memo goes live.", markdown_report)
            self.assertIn("forum, treasury", html_report)

    def test_list_presets_prints_supported_trait_groups(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--list-presets"],
            cwd=ROOT,
            env={**dict(), **{"PYTHONPATH": str(SRC)}},
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("community", result.stdout)
        self.assertIn("delegates", result.stdout)

    def test_run_report_dir_writes_full_bundle_and_tagged_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            report_dir = tmp / "artifacts" / "demo"
            scenario_path.write_text(
                json.dumps(
                    {
                        "title": "Tagged scenario bundle",
                        "summary": "Pre-forum dry run with reusable labels.",
                        "proposal_text": "Move part of the treasury budget into contributor growth experiments.",
                        "labels": ["dao", "growth", "dry-run"],
                        "participants": [
                            {"stakeholder": "DAO delegates", "group": "delegates"},
                            {"name": "Contributor circle", "trait": "contributors"},
                        ],
                    }
                ),
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
                    "--report-dir",
                    str(report_dir),
                ],
                cwd=ROOT,
                env={**dict(), **{"PYTHONPATH": str(SRC)}},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["tags"], ["dao", "growth", "dry-run"])
            self.assertTrue((report_dir / "report.json").exists())
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())
            self.assertIn("## Scenario tags", (report_dir / "report.md").read_text(encoding="utf-8"))
            self.assertIn("growth, dry-run", (report_dir / "report.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
