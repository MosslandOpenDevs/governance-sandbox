from __future__ import annotations

import argparse
import json
import sys
from html import escape
from datetime import UTC, datetime
from pathlib import Path
import re
from typing import Any


def _preset_mix_summary(responses: list[dict[str, Any]]) -> list[str]:
    counts: dict[str, int] = {}
    for response in responses:
        preset = response.get("preset")
        if not preset:
            continue
        key = str(preset).strip()
        if not key:
            continue
        counts[key] = counts.get(key, 0) + 1
    return [f"{preset}: {counts[preset]}" for preset in sorted(counts)]


from .engine import PRESET_SUMMARIES, TRAIT_PRESETS, simulate_governance

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _load_scenario(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if str(path) == "-":
        text = sys.stdin.read()
        try:
            loaded = json.loads(text)
        except json.JSONDecodeError:
            if yaml is None:
                raise SystemExit("Scenario stdin must be valid JSON unless PyYAML is installed for YAML support.")
            loaded = yaml.safe_load(text)
    else:
        text = path.read_text(encoding="utf-8")
        if suffix == ".json":
            loaded = json.loads(text)
        elif suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise SystemExit("YAML support requires PyYAML to be installed.")
            loaded = yaml.safe_load(text)
        else:
            raise SystemExit(f"Unsupported scenario file format: {path.suffix}")
    if not isinstance(loaded, dict):
        return {}
    scenario_keys = ("proposal", "proposal_text", "prompt", "stakeholders", "participants", "actors", "stakeholder_map", "stakeholder_presets", "scenario", "inputs", "report")
    nested_scenario_keys = ("proposal", "proposal_text", "prompt", "stakeholders", "participants", "actors", "stakeholder_map", "stakeholder_presets", "inputs", "report")
    for wrapper_key in ("scenario_payload", "scenario_data", "scenario_bundle", "scenario_document", "scenario_spec", "scenario_input", "scenario_inputs", "scenario_config", "scenario_plan", "scenario_manifest", "rehearsal", "rehearsal_bundle"):
        wrapped = loaded.get(wrapper_key)
        if isinstance(wrapped, dict) and any(key in wrapped for key in scenario_keys):
            nested_scenario = wrapped.get("scenario")
            if isinstance(nested_scenario, dict) and any(key in nested_scenario for key in nested_scenario_keys):
                merged = dict(nested_scenario)
                for key, value in wrapped.items():
                    if key != "scenario" and key not in merged:
                        merged[key] = value
                return merged
            return wrapped
    top_level_scenario = loaded.get("scenario")
    if isinstance(top_level_scenario, dict) and any(key in top_level_scenario for key in nested_scenario_keys):
        merged = dict(top_level_scenario)
        for key, value in loaded.items():
            if key != "scenario" and key not in merged:
                merged[key] = value
        return merged
    return loaded


def _pick(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return value
    return None


def _normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in re.split(r"[,\n]", value) if item.strip()]
    if isinstance(value, list):
        normalized: list[str] = []
        for item in value:
            if item is None:
                continue
            rendered = str(item).strip()
            if rendered:
                normalized.append(rendered)
        return normalized
    rendered = str(value).strip()
    return [rendered] if rendered else []


def _normalize_stakeholders(value: Any) -> list[str] | list[dict[str, str]]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in re.split(r"[,\n]", value) if item.strip()]
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        normalized: list[dict[str, str]] = []
        for name, preset in value.items():
            rendered_name = str(name).strip()
            if not rendered_name:
                continue
            stakeholder: dict[str, str] = {"name": rendered_name}
            if isinstance(preset, dict):
                nested_actor = _pick(preset, "stakeholder", "participant", "actor")
                if isinstance(nested_actor, dict):
                    alias_name = _pick(nested_actor, "name", "label", "title", "stakeholder", "participant", "actor")
                    if alias_name is not None and str(alias_name).strip():
                        stakeholder["name"] = str(alias_name).strip()
                    preset_name = _pick(nested_actor, "preset", "trait_preset", "trait", "persona", "group", "role", "segment", "cohort", "archetype", "preset_name", "preset_key")
                    if preset_name is not None and str(preset_name).strip():
                        stakeholder["preset"] = str(preset_name).strip()
                else:
                    alias_name = _pick(preset, "name", "label", "title", "stakeholder", "participant", "actor")
                    if alias_name is not None and str(alias_name).strip():
                        stakeholder["name"] = str(alias_name).strip()
                    preset_name = _pick(preset, "preset", "trait_preset", "trait", "persona", "group", "role", "segment", "cohort", "archetype", "preset_name", "preset_key")
                    if preset_name is not None and str(preset_name).strip():
                        stakeholder["preset"] = str(preset_name).strip()
            elif preset is not None and str(preset).strip():
                stakeholder["preset"] = str(preset).strip()
            normalized.append(stakeholder)
        return normalized
    return []


def _proposal_parts_from_mapping(value: dict[str, Any]) -> list[str]:
    title = _pick(value, "title", "name", "label", "heading", "subject", "proposal_title", "proposal_name")
    summary = _pick(value, "summary", "description", "brief", "overview", "proposal_summary", "proposal_brief")
    body = _pick(value, "body", "text", "content", "proposal", "proposal_text", "prompt", "message", "proposal_body")
    parts = [
        str(item).strip()
        for item in (title, summary, body)
        if item is not None and str(item).strip()
    ]
    bullet_values = _pick(value, "bullets", "points", "checklist", "items", "proposal_points", "proposal_bullets")
    bullet_lines = [f"- {item}" for item in _normalize_string_list(bullet_values)]
    if bullet_lines:
        parts.append("Key points:\n" + "\n".join(bullet_lines))
    section_values = _pick(value, "sections", "steps", "phases", "proposal_sections")
    if isinstance(section_values, list):
        rendered_sections: list[str] = []
        for section in section_values:
            if isinstance(section, dict):
                section_title = _pick(section, "title", "name", "label", "heading")
                section_body = _pick(section, "body", "text", "content", "summary", "description")
                section_points = [f"- {item}" for item in _normalize_string_list(_pick(section, "bullets", "points", "items", "checklist"))]
                section_parts = [
                    str(item).strip()
                    for item in (section_title, section_body)
                    if item is not None and str(item).strip()
                ]
                if section_points:
                    section_parts.append("\n".join(section_points))
                if section_parts:
                    rendered_sections.append("\n".join(section_parts))
            else:
                rendered = str(section).strip()
                if rendered:
                    rendered_sections.append(rendered)
        if rendered_sections:
            parts.append("Sections:\n" + "\n\n".join(rendered_sections))
    return parts


def _normalize_proposal(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    if isinstance(value, dict):
        parts = _proposal_parts_from_mapping(value)
        if parts:
            return "\n\n".join(parts)
    normalized = str(value).strip()
    return normalized or None


def _normalize_proposal_from_mapping(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    parts = _proposal_parts_from_mapping(value)
    if parts:
        return "\n\n".join(parts)
    return None


def _slugify_report_basename(raw: str | None) -> str:
    if not raw:
        return "report"
    slug = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower())
    slug = slug.strip("-.")
    return slug or "report"


def _resolve_report_basename(*report_sections: dict[str, Any], scenario: dict[str, Any]) -> str:
    for report_meta in report_sections:
        report_outputs = report_meta.get("outputs") if isinstance(report_meta.get("outputs"), dict) else {}
        configured = _pick(report_outputs, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name") or _pick(report_meta, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name")
        if configured:
            return _slugify_report_basename(str(configured))
    configured = _pick(scenario, "report_basename", "report_file_stem", "report_stem", "report_name")
    if configured:
        return _slugify_report_basename(str(configured))
    titled = next((
        _pick(report_meta, "title", "heading")
        for report_meta in report_sections
        if _pick(report_meta, "title", "heading")
    ), None) or _pick(scenario, "report_title")
    if titled:
        return _slugify_report_basename(str(titled))
    return "report"


def _render_markdown_report(result: dict[str, Any]) -> str:
    meta = result.get("report") or {}
    scenario = result.get("scenario") or {}
    lines = [
        f"# {scenario.get('report_title') or 'Governance Sandbox Report'}",
        "",
    ]
    summary = result.get("summary") or {}
    artifacts = meta.get("artifacts") or {}
    if meta.get("generated_at") or meta.get("scenario_file") or any(artifacts.values()):
        lines.append("## Report metadata")
        if meta.get("generated_at"):
            lines.append(f"- Generated at: {meta['generated_at']}")
        if meta.get("scenario_file"):
            lines.append(f"- Scenario file: {meta['scenario_file']}")
        if artifacts.get("directory"):
            lines.append(f"- Report directory: {artifacts['directory']}")
        if artifacts.get("basename"):
            lines.append(f"- Report basename: {artifacts['basename']}")
        if artifacts.get("json"):
            lines.append(f"- JSON artifact: {artifacts['json']}")
        if artifacts.get("markdown"):
            lines.append(f"- Markdown artifact: {artifacts['markdown']}")
        if artifacts.get("html"):
            lines.append(f"- HTML artifact: {artifacts['html']}")
        lines.append("")
    if scenario.get("name"):
        lines.extend(["## Scenario", scenario["name"], ""])
    if scenario.get("context"):
        lines.extend(["## Context", scenario["context"], ""])
    if scenario.get("report_title"):
        lines.extend(["## Report title", scenario["report_title"], ""])
    if scenario.get("report_subtitle"):
        lines.extend(["## Report subtitle", scenario["report_subtitle"], ""])
    if scenario.get("report_summary"):
        lines.extend(["## Report summary", scenario["report_summary"], ""])
    if scenario.get("report_audience"):
        lines.extend(["## Report audience", scenario["report_audience"], ""])
    if scenario.get("report_owner"):
        lines.extend(["## Report owner", scenario["report_owner"], ""])
    if scenario.get("report_subject"):
        lines.extend(["## Report subject", scenario["report_subject"], ""])
    if scenario.get("report_priority"):
        lines.extend(["## Report priority", scenario["report_priority"], ""])
    if scenario.get("scenario_file"):
        lines.extend(["## Scenario source", scenario["scenario_file"], ""])
    if scenario.get("tags"):
        lines.extend(["## Scenario tags", ", ".join(scenario["tags"]), ""])
    if summary:
        lines.extend(
            [
                "## Outcome snapshot",
                f"- Stakeholders: {summary['stakeholder_count']}",
                f"- Supportive: {summary['supportive']}",
                f"- Cautious: {summary['cautious']}",
                f"- Mixed: {summary['mixed']}",
                f"- Skeptical: {summary['skeptical']}",
                f"- Recommendation: {summary['recommendation_label']}",
            ]
        )
        preset_mix = _preset_mix_summary(result.get("responses") or [])
        if preset_mix:
            lines.append(f"- Preset mix: {', '.join(preset_mix)}")
        lines.append("")
    lines.extend([
        "## Proposal",
        result["proposal"],
        "",
        f"## Recommendation\n{result['recommendation']}",
        "",
        "## Stakeholder responses",
    ])
    for response in result["responses"]:
        preset_key = response.get("preset")
        preset = f" ({preset_key})" if preset_key else ""
        lines.extend(
            [
                f"### {response['name']}{preset}",
            ]
        )
        if preset_key and preset_key in PRESET_SUMMARIES:
            lines.append(f"- Preset summary: {PRESET_SUMMARIES[preset_key]}")
        lines.extend(
            [
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
    meta = result.get("report") or {}
    scenario = result.get("scenario") or {}
    summary = result.get("summary") or {}
    preset_mix = _preset_mix_summary(result.get("responses") or [])
    for response in result["responses"]:
        preset_key = response.get("preset")
        preset = f" <span class=\"preset\">{escape(preset_key)}</span>" if preset_key else ""
        preset_summary = (
            f'<p><strong>Preset summary:</strong> {escape(PRESET_SUMMARIES[preset_key])}</p>'
            if preset_key in PRESET_SUMMARIES
            else ""
        )
        response_cards.append(
            "".join(
                [
                    '<section class="card">',
                    f'<h3>{escape(response["name"])}{preset}</h3>',
                    preset_summary,
                    f'<p><strong>Stance:</strong> {escape(response["stance"])}</p>',
                    f'<p><strong>Concern:</strong> {escape(response["concern"])}</p>',
                    f'<p><strong>Mitigation:</strong> {escape(response["mitigation"])}</p>',
                    "</section>",
                ]
            )
        )
    risks = "".join(f"<li>{escape(risk)}</li>" for risk in result["major_risks"])
    scenario_panel = ""
    if any(scenario.get(key) for key in ("name", "context", "report_title", "report_subtitle", "report_summary", "report_audience", "report_owner", "report_subject", "report_priority", "scenario_file", "tags")):
        scenario_bits: list[str] = []
        if scenario.get("name"):
            scenario_bits.append(f'<p><strong>Scenario:</strong> {escape(scenario["name"])}</p>')
        if scenario.get("context"):
            scenario_bits.append(f'<p><strong>Context:</strong> {escape(scenario["context"])}</p>')
        if scenario.get("report_title"):
            scenario_bits.append(f'<p><strong>Report title:</strong> {escape(scenario["report_title"])}</p>')
        if scenario.get("report_subtitle"):
            scenario_bits.append(f'<p><strong>Report subtitle:</strong> {escape(scenario["report_subtitle"])}</p>')
        if scenario.get("report_summary"):
            scenario_bits.append(f'<p><strong>Report summary:</strong> {escape(scenario["report_summary"])}</p>')
        if scenario.get("report_audience"):
            scenario_bits.append(f'<p><strong>Report audience:</strong> {escape(scenario["report_audience"])}</p>')
        if scenario.get("report_owner"):
            scenario_bits.append(f'<p><strong>Report owner:</strong> {escape(scenario["report_owner"])}</p>')
        if scenario.get("report_subject"):
            scenario_bits.append(f'<p><strong>Report subject:</strong> {escape(scenario["report_subject"])}</p>')
        if scenario.get("report_priority"):
            scenario_bits.append(f'<p><strong>Report priority:</strong> {escape(scenario["report_priority"])}</p>')
        if scenario.get("scenario_file"):
            scenario_bits.append(f'<p><strong>Scenario source:</strong> {escape(scenario["scenario_file"])}</p>')
        if scenario.get("tags"):
            scenario_bits.append(f'<p><strong>Scenario tags:</strong> {escape(", ".join(scenario["tags"]))}</p>')
        scenario_panel = '<section class="panel">' + ''.join(scenario_bits) + '</section>'
    metadata_panel = ""
    artifacts = meta.get("artifacts") or {}
    if meta.get("generated_at") or meta.get("scenario_file") or any(artifacts.values()):
        metadata_bits: list[str] = []
        if meta.get("generated_at"):
            metadata_bits.append(f'<p><strong>Generated at:</strong> {escape(meta["generated_at"])}</p>')
        if meta.get("scenario_file"):
            metadata_bits.append(f'<p><strong>Scenario file:</strong> {escape(meta["scenario_file"])}</p>')
        if artifacts.get("directory"):
            metadata_bits.append(f'<p><strong>Report directory:</strong> {escape(artifacts["directory"])}</p>')
        if artifacts.get("basename"):
            metadata_bits.append(f'<p><strong>Report basename:</strong> {escape(artifacts["basename"])}</p>')
        if artifacts.get("json"):
            metadata_bits.append(f'<p><strong>JSON artifact:</strong> {escape(artifacts["json"])}</p>')
        if artifacts.get("markdown"):
            metadata_bits.append(f'<p><strong>Markdown artifact:</strong> {escape(artifacts["markdown"])}</p>')
        if artifacts.get("html"):
            metadata_bits.append(f'<p><strong>HTML artifact:</strong> {escape(artifacts["html"])}</p>')
        metadata_panel = '<section class="panel"><h2>Report metadata</h2>' + ''.join(metadata_bits) + '</section>'
    tag_panel = ""
    if scenario.get("tags"):
        tag_panel = '<section class="panel"><h2>Scenario tags</h2><p>' + ', '.join(escape(tag) for tag in scenario['tags']) + '</p></section>'
    summary_panel = ""
    if summary:
        summary_panel = ''.join([
            '<section class="panel"><h2>Outcome snapshot</h2><div class="grid">',
            f'<section class="card"><h3>{escape(str(summary["stakeholder_count"]))}</h3><p>Stakeholders</p></section>',
            f'<section class="card"><h3>{escape(str(summary["supportive"]))}</h3><p>Supportive</p></section>',
            f'<section class="card"><h3>{escape(str(summary["cautious"]))}</h3><p>Cautious</p></section>',
            f'<section class="card"><h3>{escape(str(summary["mixed"]))}</h3><p>Mixed</p></section>',
            f'<section class="card"><h3>{escape(str(summary["skeptical"]))}</h3><p>Skeptical</p></section>',
            '</div></section>',
        ])
    preset_mix_panel = ""
    if preset_mix:
        preset_mix_panel = (
            '<section class="panel"><h2>Preset mix</h2><p>'
            + escape(', '.join(preset_mix))
            + '</p></section>'
        )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(scenario.get("report_title") or "Governance Sandbox Report")}</title>
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
    <p class="badge">Recommendation: {escape(result['recommendation'])}</p>
    <h1>{escape(scenario.get("report_title") or "Governance Sandbox Report")}</h1>
    {f"<p><strong>{escape(scenario['report_subtitle'])}</strong></p>" if scenario.get("report_subtitle") else ""}
    <p>{escape(result['proposal'])}</p>
  </section>
  {metadata_panel}
  {scenario_panel}
  {tag_panel}
  {summary_panel}
  {preset_mix_panel}
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
    <p>{escape(result['decision_memo'])}</p>
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
    run_cmd.add_argument("--report-markdown", "--report-md", dest="report_markdown", help="Write a markdown report to this path")
    run_cmd.add_argument("--report-html", "--report-htm", dest="report_html", help="Write an HTML report to this path")
    run_cmd.add_argument("--report-json", help="Write the JSON result to this path")
    run_cmd.add_argument("--report-dir", help="Write report.json, report.md, and report.html into this directory")
    run_cmd.add_argument("--list-presets", action="store_true", help="List built-in stakeholder presets")
    run_cmd.add_argument("--list-presets-json", action="store_true", help="Print built-in stakeholder presets as JSON")

    args = parser.parse_args()

    if args.command == "run":
        if args.list_presets_json:
            catalog = {
                preset: {
                    "label": preset.replace("-", " ").title(),
                    "summary": PRESET_SUMMARIES.get(preset),
                    **details,
                }
                for preset, details in TRAIT_PRESETS.items()
            }
            print(json.dumps({"presets": catalog}, ensure_ascii=False, indent=2))
            return
        if args.list_presets:
            print("\n".join(sorted(TRAIT_PRESETS)))
            return
        scenario: dict[str, Any] = {}
        if args.scenario_file:
            scenario = _load_scenario(Path(args.scenario_file))
        scenario_meta = scenario.get("scenario") if isinstance(scenario.get("scenario"), dict) else {}
        inputs = scenario.get("inputs") if isinstance(scenario.get("inputs"), dict) else {}
        scenario_inputs = scenario_meta.get("inputs") if isinstance(scenario_meta.get("inputs"), dict) else {}
        inputs_report = inputs.get("report") if isinstance(inputs.get("report"), dict) else {}
        scenario_inputs_report = scenario_inputs.get("report") if isinstance(scenario_inputs.get("report"), dict) else {}
        proposal = _normalize_proposal(args.proposal) or _normalize_proposal(_pick(scenario, "proposal", "proposal_text", "prompt")) or _normalize_proposal(_pick(inputs, "proposal", "proposal_text", "prompt")) or _normalize_proposal(_pick(scenario_inputs, "proposal", "proposal_text", "prompt")) or _normalize_proposal_from_mapping(scenario) or _normalize_proposal_from_mapping(inputs) or _normalize_proposal_from_mapping(scenario_inputs)
        stakeholder_input = args.stakeholders
        if stakeholder_input:
            stakeholders: list[str] | list[dict[str, str]] = [item.strip() for item in stakeholder_input.split(",") if item.strip()]
        else:
            stakeholders = _normalize_stakeholders(
                _pick(scenario, "stakeholders", "participants", "actors", "stakeholder_groups", "voters", "stakeholder_map", "stakeholder_presets", "preset_groups", "stakeholder_preset_map", "stakeholder_traits", "stakeholder_personas", "traits", "personas")
                or _pick(inputs, "stakeholders", "participants", "actors", "stakeholder_groups", "voters", "stakeholder_map", "stakeholder_presets", "preset_groups", "stakeholder_preset_map", "stakeholder_traits", "stakeholder_personas", "traits", "personas")
                or _pick(scenario_inputs, "stakeholders", "participants", "actors", "stakeholder_groups", "voters", "stakeholder_map", "stakeholder_presets", "preset_groups", "stakeholder_preset_map", "stakeholder_traits", "stakeholder_personas", "traits", "personas")
            )
        if not proposal:
            raise SystemExit("Proposal is required via --proposal or --scenario-file")
        if not stakeholders:
            raise SystemExit("Stakeholders are required via --stakeholders or --scenario-file")
        result = simulate_governance(proposal, stakeholders)
        report_meta = scenario.get("report") if isinstance(scenario.get("report"), dict) else {}
        top_level_report_outputs = scenario.get("report_outputs") if isinstance(scenario.get("report_outputs"), dict) else {}
        report_outputs = report_meta.get("outputs") if isinstance(report_meta.get("outputs"), dict) else {}
        inputs_report_outputs = inputs_report.get("outputs") if isinstance(inputs_report.get("outputs"), dict) else {}
        scenario_inputs_report_outputs = scenario_inputs_report.get("outputs") if isinstance(scenario_inputs_report.get("outputs"), dict) else {}
        scenario_source_alias = _pick(
            scenario,
            "scenario_file",
            "scenario_source",
            "source",
            "source_file",
            "scenario_path",
            "source_path",
        ) or _pick(
            scenario_meta,
            "scenario_file",
            "scenario_source",
            "source",
            "source_file",
            "scenario_path",
            "source_path",
        ) or _pick(
            inputs,
            "scenario_file",
            "scenario_source",
            "source",
            "source_file",
            "scenario_path",
            "source_path",
        ) or _pick(
            scenario_inputs,
            "scenario_file",
            "scenario_source",
            "source",
            "source_file",
            "scenario_path",
            "source_path",
        )
        scenario_source = (
            scenario_source_alias
            if args.scenario_file == "-" and scenario_source_alias
            else (
                "stdin"
                if args.scenario_file == "-"
                else (str(Path(args.scenario_file).resolve()) if args.scenario_file else scenario_source_alias)
            )
        )
        result["scenario"] = {
            "name": _pick(scenario, "name", "title", "scenario_name", "scenario_title") or _pick(scenario_meta, "name", "title", "scenario_name", "scenario_title"),
            "context": _pick(scenario, "context", "scenario_context", "decision_context", "decision", "summary", "description") or _pick(scenario_meta, "context", "scenario_context", "decision_context", "decision", "summary", "description") or _pick(report_meta, "context", "scenario_context", "decision_context", "summary", "description") or _pick(inputs_report, "context", "scenario_context", "decision_context", "summary", "description") or _pick(scenario_inputs_report, "context", "scenario_context", "decision_context", "summary", "description"),
            "report_title": _pick(scenario, "report_title", "report_heading") or _pick(scenario_meta, "report_title", "report_heading") or _pick(report_meta, "title", "heading") or _pick(inputs_report, "title", "heading") or _pick(scenario_inputs_report, "title", "heading"),
            "report_subtitle": _pick(scenario, "report_subtitle", "report_subheading") or _pick(scenario_meta, "report_subtitle", "report_subheading") or _pick(report_meta, "subtitle", "subheading") or _pick(inputs_report, "subtitle", "subheading") or _pick(scenario_inputs_report, "subtitle", "subheading"),
            "report_summary": _pick(report_meta, "report_summary", "summary", "description", "abstract", "brief", "synopsis", "memo", "memo_summary", "executive_summary", "overview", "report_overview") or _pick(inputs_report, "report_summary", "summary", "description", "abstract", "brief", "synopsis", "memo", "memo_summary", "executive_summary", "overview", "report_overview") or _pick(scenario_inputs_report, "report_summary", "summary", "description", "abstract", "brief", "synopsis", "memo", "memo_summary", "executive_summary", "overview", "report_overview") or _pick(scenario, "report_summary", "summary", "brief", "synopsis", "memo", "memo_summary", "overview", "report_overview") or _pick(scenario_meta, "report_summary", "summary", "description", "brief", "synopsis", "memo", "memo_summary", "overview", "report_overview"),
            "report_basename": _pick(report_outputs, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name") or _pick(top_level_report_outputs, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name") or _pick(report_meta, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name") or _pick(inputs_report, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name") or _pick(scenario_inputs_report, "basename", "base_name", "file_basename", "file_stem", "stem", "output_basename", "output_name", "slug", "name") or _pick(scenario, "report_basename", "report_file_stem", "report_stem", "report_name"),
            "report_audience": ", ".join(_normalize_string_list(_pick(report_meta, "audience", "audiences", "readers", "viewers", "targets", "report_audience", "report_audiences", "report_readers", "report_viewers", "report_targets") or _pick(inputs_report, "audience", "audiences", "readers", "viewers", "targets", "report_audience", "report_audiences", "report_readers", "report_viewers", "report_targets") or _pick(scenario_inputs_report, "audience", "audiences", "readers", "viewers", "targets", "report_audience", "report_audiences", "report_readers", "report_viewers", "report_targets") or _pick(scenario, "report_audience", "report_audiences", "report_readers", "report_viewers", "report_targets", "audience", "audiences", "viewers") or _pick(scenario_meta, "report_audience", "report_audiences", "report_readers", "report_viewers", "report_targets", "audience", "audiences", "viewers"))) or None,
            "report_owner": ", ".join(_normalize_string_list(_pick(report_meta, "owner", "owners", "maintainer", "maintainers", "author", "authors", "report_owner", "report_owners", "report_author", "report_authors") or _pick(inputs_report, "owner", "owners", "maintainer", "maintainers", "author", "authors", "report_owner", "report_owners", "report_author", "report_authors") or _pick(scenario_inputs_report, "owner", "owners", "maintainer", "maintainers", "author", "authors", "report_owner", "report_owners", "report_author", "report_authors") or _pick(scenario, "report_owner", "report_owners", "report_author", "report_authors", "owner", "owners", "maintainer", "maintainers", "author", "authors") or _pick(scenario_meta, "report_owner", "report_owners", "report_author", "report_authors", "owner", "owners", "maintainer", "maintainers", "author", "authors"))) or None,
            "report_subject": ", ".join(_normalize_string_list(_pick(report_meta, "subject", "subjects", "topic", "topics", "theme", "themes", "focus", "focuses", "report_subject", "report_subjects") or _pick(inputs_report, "subject", "subjects", "topic", "topics", "theme", "themes", "focus", "focuses", "report_subject", "report_subjects") or _pick(scenario_inputs_report, "subject", "subjects", "topic", "topics", "theme", "themes", "focus", "focuses", "report_subject", "report_subjects") or _pick(scenario, "report_subject", "report_subjects", "subject", "subjects", "topic", "topics", "theme", "themes", "focus", "focuses") or _pick(scenario_meta, "report_subject", "report_subjects", "subject", "subjects", "topic", "topics", "theme", "themes", "focus", "focuses"))) or None,
            "report_priority": _pick(report_meta, "priority", "urgency", "importance", "priority_level", "priority_label", "report_priority", "report_urgency") or _pick(inputs_report, "priority", "urgency", "importance", "priority_level", "priority_label", "report_priority", "report_urgency") or _pick(scenario_inputs_report, "priority", "urgency", "importance", "priority_level", "priority_label", "report_priority", "report_urgency") or _pick(scenario, "report_priority", "report_urgency", "priority", "urgency", "importance", "priority_level", "priority_label") or _pick(scenario_meta, "report_priority", "report_urgency", "priority", "urgency", "importance", "priority_level", "priority_label"),
            "scenario_file": str(scenario_source) if scenario_source is not None else None,
            "tags": _normalize_string_list(_pick(scenario, "tags", "labels", "report_tags") or _pick(scenario_meta, "tags", "labels", "report_tags") or _pick(report_meta, "tags", "labels") or _pick(inputs_report, "tags", "labels") or _pick(scenario_inputs_report, "tags", "labels")),
        }
        counts = {stance: 0 for stance in ("supportive", "cautious", "mixed", "skeptical")}
        for response in result["responses"]:
            stance = response.get("stance")
            if stance in counts:
                counts[stance] += 1
        result["summary"] = {
            "stakeholder_count": len(result["responses"]),
            "supportive": counts["supportive"],
            "cautious": counts["cautious"],
            "mixed": counts["mixed"],
            "skeptical": counts["skeptical"],
            "recommendation_label": result["recommendation"],
        }
        result["report"] = {
            "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "scenario_file": str(scenario_source) if scenario_source is not None else None,
        }
        configured_report_dir = _pick(report_outputs, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(top_level_report_outputs, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(inputs_report_outputs, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(scenario_inputs_report_outputs, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(report_meta, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(inputs_report, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(scenario_inputs_report, "dir", "bundle_dir", "report_dir", "reports_dir", "output_dir", "output_folder", "reports_folder", "directory", "output_directory", "folder", "bundle_folder") or _pick(scenario, "report_dir", "reports_dir", "report_directory", "report_output_dir", "report_output_directory", "report_output_folder", "reports_folder", "report_bundle_dir", "report_bundle_directory", "bundle_dir", "report_folder")
        if args.report_dir:
            report_dir = Path(args.report_dir)
        elif configured_report_dir:
            report_dir = Path(str(configured_report_dir))
            if not report_dir.is_absolute() and args.scenario_file and args.scenario_file != "-":
                report_dir = Path(args.scenario_file).resolve().parent / report_dir
        else:
            report_dir = None
        report_basename = _resolve_report_basename(
            report_meta,
            top_level_report_outputs,
            inputs_report,
            scenario_inputs_report,
            scenario=result["scenario"],
        )
        configured_json_path = _pick(report_outputs, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(top_level_report_outputs, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(inputs_report_outputs, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(scenario_inputs_report_outputs, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(report_meta, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(inputs_report, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(scenario_inputs_report, "json", "json_path", "json_file", "report_json", "output_json", "json_output", "json_output_file", "output_json_file") or _pick(scenario, "report_json_path", "report_json_file", "output_json_path", "json_output")
        configured_markdown_path = _pick(report_outputs, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(top_level_report_outputs, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(inputs_report_outputs, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(scenario_inputs_report_outputs, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(report_meta, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(inputs_report, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(scenario_inputs_report, "markdown", "markdown_path", "markdown_file", "report_markdown", "output_markdown", "md", "md_path", "md_file", "markdown_output", "markdown_output_file", "output_markdown_file") or _pick(scenario, "report_markdown_path", "report_markdown_file", "output_markdown_path", "report_md_path", "md_file", "markdown_output")
        configured_html_path = _pick(report_outputs, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(top_level_report_outputs, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(inputs_report_outputs, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(scenario_inputs_report_outputs, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(report_meta, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(inputs_report, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(scenario_inputs_report, "html", "html_path", "html_file", "report_html", "output_html", "html_output", "html_output_file", "output_html_file") or _pick(scenario, "report_html_path", "report_html_file", "output_html_path", "html_output")

        def _resolve_report_path(configured: Any) -> Path | None:
            if configured is None:
                return None
            candidate = Path(str(configured))
            if not candidate.is_absolute() and args.scenario_file and args.scenario_file != "-":
                candidate = Path(args.scenario_file).resolve().parent / candidate
            return candidate

        report_json_path = _resolve_report_path(args.report_json) if args.report_json else (_resolve_report_path(configured_json_path) or (report_dir / f"{report_basename}.json" if report_dir else None))
        markdown_path = _resolve_report_path(args.report_markdown) if args.report_markdown else (_resolve_report_path(configured_markdown_path) or (report_dir / f"{report_basename}.md" if report_dir else None))
        html_path = _resolve_report_path(args.report_html) if args.report_html else (_resolve_report_path(configured_html_path) or (report_dir / f"{report_basename}.html" if report_dir else None))
        result["report"]["artifacts"] = {
            "json": str(report_json_path.resolve()) if report_json_path else None,
            "markdown": str(markdown_path.resolve()) if markdown_path else None,
            "html": str(html_path.resolve()) if html_path else None,
            "directory": str(report_dir.resolve()) if report_dir else None,
            "basename": report_basename,
        }
        markdown_report = _render_markdown_report(result)
        html_report = _render_html_report(result)
        if report_json_path:
            report_json_path.parent.mkdir(parents=True, exist_ok=True)
        if markdown_path:
            markdown_path.parent.mkdir(parents=True, exist_ok=True)
            markdown_path.write_text(markdown_report, encoding="utf-8")
        if html_path:
            html_path.parent.mkdir(parents=True, exist_ok=True)
            html_path.write_text(html_report, encoding="utf-8")
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
        if report_json_path:
            report_json_path.write_text(rendered + "\n", encoding="utf-8")
        if report_dir and report_basename != "report":
            alias_json_path = report_dir / "report.json"
            alias_markdown_path = report_dir / "report.md"
            alias_html_path = report_dir / "report.html"
            alias_json_path.parent.mkdir(parents=True, exist_ok=True)
            alias_json_path.write_text(rendered + "\n", encoding="utf-8")
            alias_markdown_path.write_text(markdown_report, encoding="utf-8")
            alias_html_path.write_text(html_report, encoding="utf-8")
        print(rendered)


if __name__ == "__main__":
    main()
