from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .engine import TRAIT_PRESETS, simulate_governance

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _load_scenario(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".json":
        return json.loads(text)
    if suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise SystemExit("YAML support requires PyYAML to be installed.")
        loaded = yaml.safe_load(text)
        return loaded if isinstance(loaded, dict) else {}
    raise SystemExit(f"Unsupported scenario file format: {path.suffix}")


def _render_markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# Governance Sandbox Report",
        "",
        "## Proposal",
        result["proposal"],
        "",
        f"## Recommendation\n{result['recommendation']}",
        "",
        "## Stakeholder responses",
    ]
    for response in result["responses"]:
        preset = f" ({response['preset']})" if response.get("preset") else ""
        lines.extend(
            [
                f"### {response['name']}{preset}",
                f"- Stance: {response['stance']}",
                f"- Concern: {response['concern']}",
                f"- Mitigation: {response['mitigation']}",
                "",
            ]
        )
    lines.append("## Major risks")
    lines.extend(f"- {risk}" for risk in result["major_risks"])
    lines.extend(["", "## Decision memo", result["decision_memo"], ""])
    return "\n".join(lines)


def _render_html_report(result: dict[str, Any]) -> str:
    response_cards: list[str] = []
    for response in result["responses"]:
        preset = f" <span class=\"preset\">{response['preset']}</span>" if response.get("preset") else ""
        response_cards.append(
            "".join(
                [
                    '<section class="card">',
                    f'<h3>{response["name"]}{preset}</h3>',
                    f'<p><strong>Stance:</strong> {response["stance"]}</p>',
                    f'<p><strong>Concern:</strong> {response["concern"]}</p>',
                    f'<p><strong>Mitigation:</strong> {response["mitigation"]}</p>',
                    "</section>",
                ]
            )
        )
    risks = "".join(f"<li>{risk}</li>" for risk in result["major_risks"])
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Governance Sandbox Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 960px; line-height: 1.6; color: #1f2937; background: #f8fafc; padding: 0 1rem; }}
    .hero, .panel, .card {{ background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1rem 1.25rem; margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; }}
    .preset {{ font-size: 0.85rem; color: #4f46e5; }}
    .badge {{ display: inline-block; padding: 0.25rem 0.6rem; border-radius: 999px; background: #e0e7ff; color: #3730a3; font-weight: 600; }}
    h1, h2, h3 {{ margin-top: 0; }}
    ul {{ padding-left: 1.25rem; }}
  </style>
</head>
<body>
  <section class="hero">
    <p class="badge">Recommendation: {result['recommendation']}</p>
    <h1>Governance Sandbox Report</h1>
    <p>{result['proposal']}</p>
  </section>
  <section class="panel">
    <h2>Major risks</h2>
    <ul>{risks}</ul>
  </section>
  <section class="panel">
    <h2>Stakeholder responses</h2>
    <div class="grid">{"".join(response_cards)}</div>
  </section>
  <section class="panel">
    <h2>Decision memo</h2>
    <p>{result['decision_memo']}</p>
  </section>
</body>
</html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(prog="gov-sandbox")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run a governance scenario rehearsal")
    run_cmd.add_argument("--proposal", help="Governance proposal text")
    run_cmd.add_argument("--stakeholders", help="Comma-separated stakeholder list")
    run_cmd.add_argument("--scenario-file", help="Path to a JSON or YAML scenario file")
    run_cmd.add_argument("--report-markdown", help="Write a markdown report to this path")
    run_cmd.add_argument("--report-html", help="Write an HTML report to this path")
    run_cmd.add_argument("--report-json", help="Write the JSON result to this path")
    run_cmd.add_argument("--list-presets", action="store_true", help="List built-in stakeholder presets")

    args = parser.parse_args()

    if args.command == "run":
        if args.list_presets:
            print("\n".join(sorted(TRAIT_PRESETS)))
            return
        scenario: dict[str, Any] = {}
        if args.scenario_file:
            scenario = _load_scenario(Path(args.scenario_file))
        proposal = args.proposal or scenario.get("proposal")
        stakeholder_input = args.stakeholders
        if stakeholder_input:
            stakeholders: list[str] | list[dict[str, str]] = [item.strip() for item in stakeholder_input.split(",") if item.strip()]
        else:
            stakeholders = scenario.get("stakeholders", [])
        if not proposal:
            raise SystemExit("Proposal is required via --proposal or --scenario-file")
        if not stakeholders:
            raise SystemExit("Stakeholders are required via --stakeholders or --scenario-file")
        result = simulate_governance(proposal, stakeholders)
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
        if args.report_json:
            Path(args.report_json).write_text(rendered + "\n", encoding="utf-8")
        if args.report_markdown:
            Path(args.report_markdown).write_text(_render_markdown_report(result), encoding="utf-8")
        if args.report_html:
            Path(args.report_html).write_text(_render_html_report(result), encoding="utf-8")
        print(rendered)


if __name__ == "__main__":
    main()
