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


class GovernanceSandboxCliTests(unittest.TestCase):

    def test_html_report_escapes_scenario_and_response_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            html_path = tmp / "report.html"
            scenario_path.write_text(
                json.dumps(
                    {
                        "name": "Treasury <review>",
                        "context": "Budget <window> & delegate alignment",
                        "proposal": "Ship <fast> & keep trust.",
                        "stakeholders": [
                            {"name": "Delegate <group>", "preset": "delegates"},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    str(scenario_path),
                    "--report-html",
                    str(html_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            html_report = html_path.read_text(encoding="utf-8")
            self.assertIn("Treasury &lt;review&gt;", html_report)
            self.assertIn("Budget &lt;window&gt; &amp; delegate alignment", html_report)
            self.assertIn("Ship &lt;fast&gt; &amp; keep trust.", html_report)
            self.assertIn("Delegate &lt;group&gt;", html_report)
            self.assertNotIn("<review>", html_report)
    def test_demo_fixture_drives_named_report_bundle_and_report_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_path = ROOT / "examples" / "scenario-web-demo.yaml"

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            basename = "treasury-confidence-rehearsal"
            self.assertEqual(payload["scenario"]["name"], "Treasury confidence rehearsal")
            self.assertEqual(payload["scenario"]["report_title"], "Treasury confidence rehearsal memo")
            self.assertEqual(payload["report"]["artifacts"]["directory"], str(report_dir.resolve()))
            self.assertEqual(payload["report"]["artifacts"]["basename"], basename)
            self.assertTrue((report_dir / f"{basename}.json").exists())
            self.assertTrue((report_dir / f"{basename}.md").exists())
            self.assertTrue((report_dir / f"{basename}.html").exists())
            self.assertTrue((report_dir / "report.json").exists())
            self.assertTrue((report_dir / "report.md").exists())
            self.assertTrue((report_dir / "report.html").exists())
            self.assertIn("## Outcome snapshot", (report_dir / f"{basename}.md").read_text(encoding="utf-8"))
            self.assertIn("Treasury confidence rehearsal memo", (report_dir / f"{basename}.html").read_text(encoding="utf-8"))

    def test_markdown_report_bundle_supports_json_fixture_example(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_path = ROOT / "examples" / "scenario-markdown-report.json"

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            basename = "markdown-bundle-rehearsal"
            self.assertEqual(payload["scenario"]["name"], "Markdown bundle rehearsal")
            self.assertEqual(payload["report"]["artifacts"]["basename"], basename)
            self.assertTrue((report_dir / f"{basename}.json").exists())
            self.assertTrue((report_dir / f"{basename}.md").exists())
            self.assertTrue((report_dir / f"{basename}.html").exists())
            self.assertIn("Markdown bundle rehearsal memo", (report_dir / f"{basename}.md").read_text(encoding="utf-8"))
            self.assertIn("governance reviewers", (report_dir / f"{basename}.md").read_text(encoding="utf-8"))

    def test_report_bundle_supports_json_fixture_example(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_path = ROOT / "examples" / "scenario-report-bundle.json"

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "JSON treasury confidence rehearsal")
            self.assertEqual(payload["scenario"]["report_title"], "JSON treasury confidence memo")
            self.assertEqual(payload["scenario"]["report_summary"], "JSON fixture proving scenario-file input plus markdown/html/json report bundle output.")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "json-treasury-confidence")
            self.assertTrue((report_dir / "json-treasury-confidence.json").exists())
            self.assertTrue((report_dir / "json-treasury-confidence.md").exists())
            self.assertTrue((report_dir / "json-treasury-confidence.html").exists())

    def test_example_preset_bundle_fixture_runs_with_report_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_path = ROOT / "examples" / "scenario-preset-bundle.yaml"

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Delegate confidence rehearsal")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-confidence-rehearsal")
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertEqual(payload["responses"][1]["preset"], "delegates")
            self.assertTrue((report_dir / "delegate-confidence-rehearsal.md").exists())
            self.assertTrue((report_dir / "delegate-confidence-rehearsal.html").exists())
            self.assertTrue((report_dir / "delegate-confidence-rehearsal.json").exists())

    def test_run_resolves_relative_cli_report_paths_from_scenario_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_dir = tmp / "fixtures"
            scenario_dir.mkdir()
            scenario_path = scenario_dir / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a staged treasury automation memo before execution.
stakeholders:
  - name: Delegate council
    preset: delegates
  - name: Builder guild
    preset: contributors
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
                    "outputs/delegate-brief.md",
                    "--report-html",
                    "outputs/delegate-brief.html",
                    "--report-json",
                    "outputs/delegate-brief.json",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            outputs_dir = scenario_dir / "outputs"
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str((outputs_dir / "delegate-brief.md").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["html"], str((outputs_dir / "delegate-brief.html").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["json"], str((outputs_dir / "delegate-brief.json").resolve()))
            self.assertTrue((outputs_dir / "delegate-brief.md").exists())
            self.assertTrue((outputs_dir / "delegate-brief.html").exists())
            self.assertTrue((outputs_dir / "delegate-brief.json").exists())

    def test_run_supports_scenario_name_and_context_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """scenario_name: Treasury runway checkpoint
scenario_context: Stress-test the rollout narrative before the vote.
proposal: Publish a staged treasury automation memo before execution.
stakeholders:
  - name: Delegate council
    preset: delegates
report:
  title: Treasury runway checkpoint memo
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Treasury runway checkpoint")
            self.assertEqual(payload["scenario"]["context"], "Stress-test the rollout narrative before the vote.")
            markdown_report = markdown_path.read_text(encoding="utf-8")
            self.assertIn("## Scenario\nTreasury runway checkpoint", markdown_report)
            self.assertIn("## Context\nStress-test the rollout narrative before the vote.", markdown_report)

    def test_run_supports_stakeholder_group_alias_and_report_reader_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """name: Alias-rich rehearsal
proposal: Stage a treasury runway checkpoint before execution.
stakeholder_groups:
  - name: DAO board
    preset: dao
  - name: Builder circle
    preset: contributors
report:
  readers:
    - delegates
    - contributors
  tags: governance, treasury, runway
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_audience"], "delegates, contributors")
            self.assertEqual(payload["scenario"]["tags"], ["governance", "treasury", "runway"])
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertEqual(payload["responses"][1]["preset"], "contributors")
            markdown_report = markdown_path.read_text(encoding="utf-8")
            self.assertIn("## Report audience\ndelegates, contributors", markdown_report)
            self.assertIn("## Scenario tags\ngovernance, treasury, runway", markdown_report)

    def test_run_supports_mapping_style_stakeholders_with_stakeholder_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a delegate-ready treasury checkpoint before voting.
stakeholders:
  reviewer-a:
    stakeholder: Delegate council
    role: delegates
  reviewer-b:
    stakeholder: Investor guild
    cohort: investors
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
            self.assertEqual(payload["responses"][0]["name"], "Delegate council")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["name"], "Investor guild")
            self.assertEqual(payload["responses"][1]["preset"], "investors")

    def test_run_supports_mapping_style_stakeholders_with_archetype_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """proposal: Publish a delegate-ready treasury checkpoint before voting.
stakeholders:
  DAO council:
    archetype: dao
  Investor guild:
    cohort: investors
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
            self.assertEqual(payload["responses"][0]["name"], "DAO council")
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertEqual(payload["responses"][1]["name"], "Investor guild")
            self.assertEqual(payload["responses"][1]["preset"], "investors")

    def test_run_supports_mapping_style_stakeholders_in_scenario_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_path = tmp / "report.md"
            scenario_path.write_text(
                """name: Mapping-style stakeholder import
proposal: Publish a delegate-ready treasury checkpoint before voting.
stakeholders:
  DAO council: dao
  Delegate cohort: delegates
report:
  title: Mapping-style stakeholder import memo
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
                    str(report_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Mapping-style stakeholder import")
            self.assertEqual(payload["responses"][0]["name"], "DAO council")
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertEqual(payload["responses"][1]["name"], "Delegate cohort")
            self.assertEqual(payload["responses"][1]["preset"], "delegates")
            markdown_report = report_path.read_text(encoding="utf-8")
            self.assertIn("### DAO council (dao)", markdown_report)
            self.assertIn("### Delegate cohort (delegates)", markdown_report)

    def test_run_supports_proposal_object_in_scenario_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                json.dumps(
                    {
                        "name": "Proposal object rehearsal",
                        "proposal": {
                            "title": "Treasury checkpoint proposal",
                            "summary": "Replay before the forum post.",
                            "body": "Add milestone-based treasury checkpoints before execution."
                        },
                        "stakeholders": [
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            expected = "Treasury checkpoint proposal\n\nReplay before the forum post.\n\nAdd milestone-based treasury checkpoints before execution."
            self.assertEqual(payload["proposal"], expected)
            self.assertIn(expected, markdown_path.read_text(encoding="utf-8"))

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
                        "report": {
                            "description": "Memo for delegates comparing treasury discipline, growth urgency, and stakeholder trust.",
                        },
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["proposal"], "Shift part of the treasury budget to community growth experiments.")
            self.assertEqual(payload["scenario"]["name"], "Treasury reallocation dry run")
            self.assertEqual(payload["scenario"]["context"], "Emergency budget review before the next DAO vote.")
            self.assertEqual(payload["scenario"]["report_summary"], "Memo for delegates comparing treasury discipline, growth urgency, and stakeholder trust.")
            self.assertEqual(payload["responses"][0]["preset"], "dao")
            self.assertEqual(payload["report"]["scenario_file"], str(scenario_path.resolve()))
            self.assertRegex(payload["report"]["generated_at"], r"Z$")
            self.assertEqual(payload["report"]["artifacts"]["json"], str(json_path.resolve()))
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str(markdown_path.resolve()))
            self.assertEqual(payload["report"]["artifacts"]["html"], str(html_path.resolve()))
            self.assertIsNone(payload["report"]["artifacts"]["directory"])
            self.assertEqual(payload["report"]["artifacts"]["basename"], "report")
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertTrue(json_path.exists())
            markdown_report = markdown_path.read_text(encoding="utf-8")
            html_report = html_path.read_text(encoding="utf-8")
            self.assertIn("# Governance Sandbox Report", markdown_report)
            self.assertIn("## Report metadata", markdown_report)
            self.assertIn(f"- Scenario file: {scenario_path.resolve()}", markdown_report)
            self.assertIn(f"- JSON artifact: {json_path.resolve()}", markdown_report)
            self.assertIn(f"- Markdown artifact: {markdown_path.resolve()}", markdown_report)
            self.assertIn(f"- HTML artifact: {html_path.resolve()}", markdown_report)
            self.assertIn("## Scenario\nTreasury reallocation dry run", markdown_report)
            self.assertIn("## Context\nEmergency budget review before the next DAO vote.", markdown_report)
            self.assertIn("## Report summary\nMemo for delegates comparing treasury discipline, growth urgency, and stakeholder trust.", markdown_report)
            self.assertIn("### DAO council (dao)", markdown_report)
            self.assertIn("<title>Governance Sandbox Report</title>", html_report)
            self.assertIn("<h2>Report metadata</h2>", html_report)
            self.assertIn(f"<strong>Scenario file:</strong> {scenario_path.resolve()}", html_report)
            self.assertIn(f"<strong>JSON artifact:</strong> {json_path.resolve()}", html_report)
            self.assertIn(f"<strong>Markdown artifact:</strong> {markdown_path.resolve()}", html_report)
            self.assertIn(f"<strong>HTML artifact:</strong> {html_path.resolve()}", html_report)
            self.assertIn("<strong>Scenario:</strong> Treasury reallocation dry run", html_report)
            self.assertIn("<strong>Report summary:</strong> Memo for delegates comparing treasury discipline, growth urgency, and stakeholder trust.", html_report)
            self.assertIn("Recommendation: Proceed with revision", html_report)
            self.assertIn("DAO council", html_report)

    def test_run_supports_stakeholder_segment_and_cohort_preset_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """name: Segment alias rehearsal
proposal: Stage delegate review before treasury execution.
stakeholders:
  - name: Community circle
    segment: community
  - name: Investor guild
    cohort: investors
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
            self.assertEqual(payload["responses"][0]["preset"], "community")
            self.assertEqual(payload["responses"][0]["stance"], "skeptical")
            self.assertEqual(payload["responses"][1]["preset"], "investors")
            self.assertEqual(payload["responses"][1]["stance"], "supportive")

    def test_run_supports_report_audience_metadata_in_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            scenario_path.write_text(
                """scenario:
  name: Audience rehearsal
report_audience: Community delegates preparing a treasury vote.
inputs:
  proposal: Add milestone checkpoints before treasury disbursements.
  stakeholders:
    - name: Delegate circle
      preset: delegates
report:
  audience: Delegate forum reviewers
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_audience"], "Delegate forum reviewers")
            self.assertIn("## Report audience\nDelegate forum reviewers", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("<strong>Report audience:</strong> Delegate forum reviewers", html_path.read_text(encoding="utf-8"))

    def test_run_supports_report_audiences_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """scenario:
  name: Audience aliases rehearsal
  report_audiences:
    - delegates
    - treasury stewards
proposal: Add staged treasury checkpoints before execution.
stakeholders:
  - name: Delegate circle
    preset: delegates
report:
  audiences:
    - forum reviewers
    - ops stewards
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_audience"], "forum reviewers, ops stewards")
            self.assertIn("## Report audience\nforum reviewers, ops stewards", markdown_path.read_text(encoding="utf-8"))

    def test_run_supports_report_targets_and_report_tags_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            scenario_path.write_text(
                """scenario:
  name: Target alias rehearsal
  report_targets:
    - delegate stewards
    - treasury reviewers
proposal: Add staged treasury release checkpoints.
stakeholders:
  - name: Delegate circle
    preset: delegates
report_tags:
  - treasury
  - rollout
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_audience"], "delegate stewards, treasury reviewers")
            self.assertEqual(payload["scenario"]["tags"], ["treasury", "rollout"])
            self.assertIn("## Report audience\ndelegate stewards, treasury reviewers", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("## Scenario tags\ntreasury, rollout", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("<strong>Report audience:</strong> delegate stewards, treasury reviewers", html_path.read_text(encoding="utf-8"))

    def test_run_supports_report_memo_summary_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """name: Memo alias rehearsal
proposal: Add staged voting checkpoints before treasury actions.
report:
  memo_summary: Memo alias summary for delegate review.
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
                    "--report-markdown",
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_summary"], "Memo alias summary for delegate review.")
            self.assertIn("## Report summary\nMemo alias summary for delegate review.", markdown_path.read_text(encoding="utf-8"))
    def test_run_supports_nested_report_summary_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """name: Nested report summary rehearsal
proposal: Gate treasury experiments behind a delegate review window.
report:
  report_summary: Nested report summary alias for markdown/html memo output.
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
                    "--report-markdown",
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_summary"], "Nested report summary alias for markdown/html memo output.")
            self.assertIn("## Report summary\nNested report summary alias for markdown/html memo output.", markdown_path.read_text(encoding="utf-8"))


    def test_run_supports_report_output_basename_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_path = ROOT / "examples" / "scenario-report-basename.yaml"

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_summary"], "Rehearsal bundle proving title plus explicit basename control.")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-memo-bundle")
            self.assertTrue((report_dir / "delegate-memo-bundle.json").exists())
            self.assertTrue((report_dir / "delegate-memo-bundle.md").exists())
            self.assertTrue((report_dir / "delegate-memo-bundle.html").exists())

    def test_run_supports_report_path_aliases_inside_scenario_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """scenario:
  name: Scenario-path rehearsal
report:
  title: Scenario-path memo
  json_path: artifacts/outputs/rehearsal.json
  markdown_path: artifacts/outputs/rehearsal.md
  html_path: artifacts/outputs/rehearsal.html
inputs:
  proposal: Add stage gates before treasury releases.
  stakeholders:
    - name: Delegate circle
      preset: delegates
    - name: Contributor pod
      preset: contributors
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
            report_root = scenario_path.parent / "artifacts" / "outputs"
            self.assertEqual(payload["scenario"]["report_title"], "Scenario-path memo")
            self.assertEqual(payload["report"]["artifacts"]["json"], str((report_root / "rehearsal.json").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["markdown"], str((report_root / "rehearsal.md").resolve()))
            self.assertEqual(payload["report"]["artifacts"]["html"], str((report_root / "rehearsal.html").resolve()))
            self.assertTrue((report_root / "rehearsal.json").exists())
            self.assertTrue((report_root / "rehearsal.md").exists())
            self.assertTrue((report_root / "rehearsal.html").exists())

    def test_run_supports_yaml_stdin_scenario_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            markdown_path = Path(tmpdir) / "stdin-report.md"
            scenario_text = """name: Stdin rehearsal
proposal: Stage contributor review before the final treasury vote.
stakeholders:
  - name: Delegate circle
    preset: delegates
  - name: Contributor guild
    preset: contributors
report:
  description: Stdin-driven rehearsal for quick review.
"""

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                input=scenario_text,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Stdin rehearsal")
            self.assertEqual(payload["scenario"]["report_summary"], "Stdin-driven rehearsal for quick review.")
            self.assertEqual(payload["report"]["scenario_file"], "stdin")
            self.assertIn("## Scenario\nStdin rehearsal", markdown_path.read_text(encoding="utf-8"))

    def test_readme_mentions_web_demo_form_to_card_scope_doc(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/WEB_DEMO_FORM_TO_CARD_SCOPE.md", readme)
        self.assertTrue((ROOT / "docs" / "WEB_DEMO_FORM_TO_CARD_SCOPE.md").exists())

    def test_example_community_feedback_scenario_uses_all_trait_presets(self) -> None:
        import yaml

        scenario_path = ROOT / "examples" / "scenario-community-feedback.yaml"
        payload = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))

        self.assertEqual(payload["report"]["name"], "community-feedback-memo")
        self.assertEqual(
            [item["preset"] for item in payload["stakeholders"]],
            ["dao", "delegates", "contributors", "investors", "community"],
        )

    def test_example_dao_report_bundle_json_fixture_is_named_and_readme_visible(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        scenario_path = ROOT / "examples" / "scenario-dao-report-bundle.json"
        payload = json.loads(scenario_path.read_text(encoding="utf-8"))

        self.assertIn("examples/scenario-dao-report-bundle.json", readme)
        self.assertEqual(payload["report"]["name"], "dao-report-bundle-replay")
        self.assertEqual([item["preset"] for item in payload["stakeholders"]], ["dao", "delegates", "contributors"])

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
report:
  name: delegate-dry-run
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Delegate sentiment rehearsal")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertIsNone(payload["report"]["artifacts"]["directory"])
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-dry-run")
            self.assertTrue(markdown_path.exists())
            self.assertTrue(html_path.exists())
            self.assertTrue(json_path.exists())
            self.assertIn("Community stewards", markdown_path.read_text(encoding="utf-8"))

    def test_report_dir_uses_report_name_alias_for_default_bundle_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """name: Investors call dry run
proposal: Publish a staged treasury transparency dashboard update.
report:
  name: investor-review-bundle
stakeholders:
  - name: Investor cohort
    preset: investors
  - name: Delegate leads
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "investor-review-bundle")
            self.assertTrue((report_dir / "investor-review-bundle.json").exists())
            self.assertTrue((report_dir / "investor-review-bundle.md").exists())
            self.assertTrue((report_dir / "investor-review-bundle.html").exists())

    def test_report_dir_supports_output_name_alias_and_top_level_report_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            report_dir = tmp / "bundle"
            scenario_path = tmp / "scenario.yaml"
            scenario_path.write_text(
                """name: Output alias rehearsal
proposal: Publish a staged delegate feedback window before execution.
report_name: top-level-fallback
report:
  output_name: reviewer-ready-memo
stakeholders:
  - name: Delegate pod
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["report"]["artifacts"]["basename"], "reviewer-ready-memo")
            self.assertTrue((report_dir / "reviewer-ready-memo.json").exists())
            self.assertTrue((report_dir / "reviewer-ready-memo.md").exists())
            self.assertTrue((report_dir / "reviewer-ready-memo.html").exists())

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                input=scenario_payload,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Stdin scenario")
            self.assertEqual(payload["report"]["scenario_file"], "stdin")
            self.assertIn("- Scenario file: stdin", markdown_path.read_text(encoding="utf-8"))

    def test_run_supports_yaml_stdin_scenario_with_nested_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            html_path = tmp / "report.html"
            scenario_payload = """scenario:
  name: YAML stdin rehearsal
  decision_context: Replayable stdin import for governance dry runs.
inputs:
  proposal: Add milestone checkpoints before treasury disbursements.
  stakeholders:
    - stakeholder: DAO delegates
      group: delegates
    - name: Community pod
      trait: community
"""

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "run",
                    "--scenario-file",
                    "-",
                    "--report-html",
                    str(html_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                input=scenario_payload,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "YAML stdin rehearsal")
            self.assertEqual(payload["scenario"]["context"], "Replayable stdin import for governance dry runs.")
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "community")
            self.assertEqual(payload["report"]["scenario_file"], "stdin")
            self.assertIn("<strong>Scenario:</strong> YAML stdin rehearsal", html_path.read_text(encoding="utf-8"))

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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

    def test_run_report_dir_supports_report_basename_from_scenario_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "artifacts" / "bundle"
            scenario_path.write_text(
                """scenario:
  name: Delegate packet rehearsal
report:
  basename: delegate-packet
inputs:
  proposal: Add milestone-based reporting to the ecosystem budget.
  stakeholders:
    - name: Delegate bench
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["name"], "Delegate packet rehearsal")
            self.assertTrue((report_dir / "delegate-packet.json").exists())
            self.assertTrue((report_dir / "delegate-packet.md").exists())
            self.assertTrue((report_dir / "delegate-packet.html").exists())

    def test_run_report_dir_sanitizes_configured_report_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """report:
  basename: ../Delegate Packet / Final
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
""",
                encoding="utf-8",
            )

            subprocess.run(
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertTrue((report_dir / "delegate-packet-final.json").exists())
            self.assertTrue((report_dir / "delegate-packet-final.md").exists())
            self.assertTrue((report_dir / "delegate-packet-final.html").exists())
            self.assertFalse((tmp / "Delegate Packet " / " Final.json").exists())

    def test_run_report_dir_uses_report_title_as_default_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            report_dir = tmp / "bundle"
            scenario_path.write_text(
                """scenario:
  name: Delegate packet rehearsal
report:
  title: Delegate Packet Final
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
""",
                encoding="utf-8",
            )

            subprocess.run(
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertTrue((report_dir / "delegate-packet-final.json").exists())
            self.assertTrue((report_dir / "delegate-packet-final.md").exists())
            self.assertTrue((report_dir / "delegate-packet-final.html").exists())

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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


    def test_run_supports_report_subtitle_metadata_in_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            html_path = tmp / "report.html"
            scenario_path.write_text(
                """scenario:
  name: Subtitle rehearsal
report:
  title: Delegate-ready memo
  subtitle: One-screen replay proving subtitle metadata in markdown and html.
inputs:
  proposal: Add milestone checkpoints before treasury automation.
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
                    "--report-markdown",
                    str(markdown_path),
                    "--report-html",
                    str(html_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_subtitle"], "One-screen replay proving subtitle metadata in markdown and html.")
            self.assertIn("## Report subtitle\nOne-screen replay proving subtitle metadata in markdown and html.", markdown_path.read_text(encoding="utf-8"))
            html_report = html_path.read_text(encoding="utf-8")
            self.assertIn("<strong>One-screen replay proving subtitle metadata in markdown and html.</strong>", html_report)
            self.assertIn("<strong>Report subtitle:</strong> One-screen replay proving subtitle metadata in markdown and html.", html_report)

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["context"], "Dry run before a forum memo goes live.")
            self.assertEqual(payload["scenario"]["report_title"], "Governance memo for delegates")
            self.assertEqual(payload["scenario"]["report_summary"], "Dry run before a forum memo goes live.")
            self.assertEqual(payload["scenario"]["tags"], ["forum", "treasury"])
            markdown_report = (report_dir / "report.md").read_text(encoding="utf-8")
            html_report = (report_dir / "report.html").read_text(encoding="utf-8")
            self.assertIn("# Governance memo for delegates", markdown_report)
            self.assertIn("## Context\nDry run before a forum memo goes live.", markdown_report)
            self.assertIn("## Report summary\nDry run before a forum memo goes live.", markdown_report)
            self.assertIn("<strong>Report summary:</strong> Dry run before a forum memo goes live.", html_report)
            self.assertIn("forum, treasury", html_report)

    def test_run_supports_report_block_context_alias_without_scenario_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """scenario:
  name: Delegate report rehearsal
report:
  title: Governance memo for delegates
  description: Report-first context for a delegate memo.
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
                    "--report-markdown",
                    str(markdown_path),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["context"], "Report-first context for a delegate memo.")
            self.assertIn("## Context\nReport-first context for a delegate memo.", markdown_path.read_text(encoding="utf-8"))

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

    def test_list_presets_json_includes_labels_and_summaries(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--list-presets-json"],
            cwd=ROOT,
            env={**dict(), **{"PYTHONPATH": str(SRC)}},
            capture_output=True,
            text=True,
            check=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["presets"]["dao"]["label"], "Dao")
        self.assertIn("mandate clarity", payload["presets"]["dao"]["summary"])
        self.assertEqual(payload["presets"]["community"]["stance"], "skeptical")

    def test_list_presets_json_prints_supported_trait_groups(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "governance_sandbox.cli", "run", "--list-presets-json"],
            cwd=ROOT,
            env={**dict(), **{"PYTHONPATH": str(SRC)}},
            capture_output=True,
            text=True,
            check=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(sorted(payload["presets"].keys()), ["community", "contributors", "dao", "delegates", "investors"])
        self.assertEqual(payload["presets"]["delegates"]["stance"], "cautious")

    def test_run_supports_role_alias_for_trait_presets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Stage a delegate check before treasury execution.",
                        "stakeholders": [
                            {"name": "Delegate council", "role": "delegates"},
                            {"name": "Community pod", "role": "community"},
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "community")

    def test_run_supports_persona_alias_for_trait_presets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Stage a delegate check before treasury execution.",
                        "stakeholders": [
                            {"name": "Delegate council", "persona": "delegates"},
                            {"name": "Community pod", "persona": "community"},
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "community")

    def test_run_supports_preset_name_and_preset_key_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.json"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Stage a delegate check before treasury execution.",
                        "stakeholders": [
                            {"name": "Delegate council", "preset_name": "delegates"},
                            {"name": "Investor pod", "preset_key": "investors"},
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "investors")

    def test_run_supports_role_and_archetype_aliases_plus_report_brief(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scenario_path = tmp / "scenario.yaml"
            markdown_path = tmp / "report.md"
            scenario_path.write_text(
                """scenario:
  name: Alias rehearsal
  brief: Compact delegate-ready summary.
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - stakeholder: Delegate lane
      role: delegates
    - name: Investor lane
      archetype: investors
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
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["responses"][0]["preset"], "delegates")
            self.assertEqual(payload["responses"][1]["preset"], "investors")
            self.assertEqual(payload["scenario"]["report_summary"], "Compact delegate-ready summary.")
            self.assertIn("## Report summary\nCompact delegate-ready summary.", markdown_path.read_text(encoding="utf-8"))

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
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

    def test_report_dir_supports_report_file_stem_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "bundle"
            scenario_path = ROOT / "examples" / "scenario-report-file-stem.yaml"

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
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_title"], "Delegate review packet")
            self.assertEqual(payload["report"]["artifacts"]["basename"], "delegate-review-packet")
            self.assertTrue((report_dir / "delegate-review-packet.json").exists())
            self.assertTrue((report_dir / "delegate-review-packet.md").exists())
            self.assertTrue((report_dir / "delegate-review-packet.html").exists())


if __name__ == "__main__":
    unittest.main()

    def test_scenario_file_accepts_persona_alias_for_trait_preset(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_path = tmp_path / "scenario.json"
            scenario_path.write_text(
                json.dumps({
                    "proposal": "Create a treasury dashboard",
                    "stakeholders": [{"name": "Delegate Council", "persona": "delegates"}],
                }),
                encoding="utf-8",
            )

            payload = cli._load_scenario_file(scenario_path)

            self.assertEqual(payload["stakeholders"][0]["persona"], "delegates")
            report = simulate_governance(payload["proposal"], payload["stakeholders"])
            self.assertEqual(report["responses"][0]["preset"], "delegates")

    def test_readme_mentions_dao_treasury_automation_example(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/dao-treasury-automation.yaml", readme)
        self.assertTrue((ROOT / "examples" / "dao-treasury-automation.yaml").exists())

    def test_report_summary_accepts_brief_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            scenario_path = tmp_path / "scenario.json"
            scenario_path.write_text(
                json.dumps({
                    "proposal": "Fund community grants",
                    "brief": "Short demo brief",
                    "stakeholders": ["community"],
                }),
                encoding="utf-8",
            )
            json_out = tmp_path / "report.json"
            markdown_out = tmp_path / "report.md"

            exit_code = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "governance_sandbox.cli",
                    "simulate",
                    "--scenario-file",
                    str(scenario_path),
                    "--json-out",
                    str(json_out),
                    "--report-file",
                    str(markdown_out),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONPATH": str(SRC)},
            )

            self.assertEqual(exit_code.returncode, 0, exit_code.stderr)
            self.assertIn("Short demo brief", markdown_out.read_text(encoding="utf-8"))

    def test_report_summary_accepts_overview_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scenario_path = Path(tmpdir) / "scenario.json"
            markdown_out = Path(tmpdir) / "report.md"
            scenario_path.write_text(
                json.dumps(
                    {
                        "proposal": "Ship treasury dashboard pilot.",
                        "stakeholders": [
                            {"name": "Delegate", "traits": {"risk": "low", "speed": "medium", "decentralization": "high"}}
                        ],
                        "report": {"overview": "Overview alias for the report summary."},
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
                    str(markdown_out),
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=ROOT,
                env=_cli_env(),
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scenario"]["report_summary"], "Overview alias for the report summary.")
            self.assertIn("Overview alias for the report summary.", markdown_out.read_text(encoding="utf-8"))

    def test_list_presets_includes_governance_trait_groups(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "governance_sandbox.cli",
                "run",
                "--list-presets",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(SRC)},
        )

        payload = json.loads(result.stdout)
        self.assertEqual(sorted(payload["presets"].keys()), ["community", "contributors", "dao", "delegates", "investors"])

