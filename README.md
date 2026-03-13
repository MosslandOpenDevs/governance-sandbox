# governance-sandbox

Agent-based governance scenario rehearsal engine for testing proposals, stakeholder reactions, and decision risks before real-world execution.

If you need a stdin-first replay note for piping one JSON or YAML scenario directly into report generation, open `docs/SCENARIO_STDIN_JSON_YAML_NOTE.md`.
If you want a ready-to-run JSON scenario file that exercises proposal import plus report generation together, open `examples/delegate-ready-rehearsal.json`.
If you want a ready-to-run JSON scenario file that proves one named markdown/html/json report bundle from scenario input, open `examples/dao-growth-report-bundle.json`.
If you need the matching maintainer note for that scenario-file-plus-report-bundle example, open `docs/SCENARIO_FILE_REPORT_EXAMPLE_NOTE.md`.
If you need a compact note for the `report.reviewers` alias while keeping the same markdown/html/json report audience output, open `docs/GOVERNANCE_SANDBOX_REPORT_REVIEWERS_ALIAS_NOTE.md`.
If your scenario file uses `report_lead` or `report_leads`, the same markdown/html/json report flow now resolves those aliases into the rendered report owner field.
Scenario files can also use `report_reviewer_list` or `report_reviewer_lists` when one workshop export keeps reviewer handoff under a list-shaped alias but should still render the same markdown/html/json report reviewers field.
If you need the matching short-alias note, open `docs/SCENARIO_REPORT_LEAD_ALIAS_NOTE.md`.
If you need a compact note for carrying `report_synopsis` into the same markdown/html/json memo-summary lane, open `docs/SCENARIO_REPORT_SYNOPSIS_ALIAS_NOTE.md`.
Scenario files can also use `proposal_copy_md` as a compact alias when proposal body text comes from markdown-oriented exports.
Scenario files can also use `proposal_copy_file` when the proposal body lives in a neighboring markdown file but the scenario bundle should stay JSON/YAML-first.
If you need the singular form for one primary memo reader, `report.reviewer` and top-level `report_reviewer` resolve to the same rendered report audience field.
If you want the smallest scenario-file-first workflow, open `docs/SCENARIO_FILE_REPORT_BUNDLE_START.md` to generate markdown/html/json outputs from one JSON or YAML input bundle.
If you need a compact phase-one reminder to keep scenario-file input and markdown/html/json report output paired as the minimum believable governance slice, open `docs/SCENARIO_PHASE_ONE_MINIMUM_PAIR_NOTE.md`.
If you need a compact phase-one cue that the first governance win is still scenario-file input plus generated report artifacts before presets or web-demo polish, open `docs/SCENARIO_REPORT_PHASE_ONE_PAIR_NOTE.md`.
If your exported scenario bundle names artifact paths as `json_report_path`, `markdown_report_path`, or `html_report_path`, the same scenario-file report flow still resolves them without reshaping the file first.
Top-level scenario fixtures can now also point straight at `report_json_file`, `report_md_file`, and `report_html_file` when one imported rehearsal should regenerate a named JSON/Markdown/HTML bundle without extra path reshaping.
If your scenario file prefers a shared basename alias like `report_bundle_slug`, the same report flow now reuses it for JSON, Markdown, and HTML artifact generation.
If you prefer a clearer owner-facing basename field, `report_bundle_name` now feeds the same JSON, Markdown, and HTML report bundle.
If you prefer a terse machine-facing basename field, `report_bundle_key` now drives the same JSON, Markdown, and HTML report bundle.
If you prefer an ID-style basename field from scenario exports, `report_bundle_id` now drives the same JSON, Markdown, and HTML report bundle.
If you prefer a reference-style basename field from scenario exports, `report_bundle_ref` now drives the same JSON, Markdown, and HTML report bundle.
If you prefer a code-style basename field from scenario exports, `report_bundle_code` now drives the same JSON, Markdown, and HTML report bundle.
If you prefer a tag-style basename field from scenario exports, `report_bundle_tag` now drives the same JSON, Markdown, and HTML report bundle.
If you prefer a plain basename field from scenario exports, `report_bundle_basename` now drives the same JSON, Markdown, and HTML report bundle.

> Rehearse governance decisions in a simulated stakeholder environment before you ship them to reality.

---

## The problem

Governance decisions often fail not because the proposal is invalid, but because stakeholders react in unexpected ways, communication breaks down, or second-order effects are ignored.

`governance-sandbox` is designed to help teams rehearse proposals before launch by simulating stakeholder perspectives, surfacing likely tensions, and generating a structured decision memo.

---

## Demo Preview

- Demo concept: scenario input → stakeholder simulation → decision memo
- Planned live demo: `docs/assets/examples/demo-link.md`
- Current MVP output: local CLI-generated governance rehearsal report

<table>
<tr>
<td><img src="./docs/assets/screenshot-1.svg" alt="Scenario input" width="100%"/></td>
<td><img src="./docs/assets/screenshot-2.svg" alt="Stakeholder simulation" width="100%"/></td>
<td><img src="./docs/assets/screenshot-3.svg" alt="Decision memo" width="100%"/></td>
</tr>
</table>

---

## 3-step how it works

### 1) Input a governance proposal
Provide a short proposal description, target decision context, and optional constraints.

### 2) Simulate stakeholder responses
The engine generates multiple stakeholder perspectives and predicts likely support, concern, or resistance patterns.

### 3) Produce a decision memo
The system outputs a structured memo with risks, tensions, recommended mitigations, and a go/no-go style summary.

---

Preset aliases now also accept `daos`, `delegation`, `contributors-core`, `investor-relations`, and `community-members` inside scenario files so JSON/YAML rehearsal packs can stay closer to real stakeholder labels without losing deterministic trait presets.

## Sample scenario

Scenario files can also include an optional scenario name and decision context that appear in markdown/html reports.
If you need the matching alias note for `scenario_label` or `scenario_heading`, open `docs/SCENARIO_LABEL_ALIAS_NOTE.md`.
Scenario wrappers can also use `scenario_stage_pack` or `scenario_stage_pack_bundle` when the same JSON/YAML rehearsal bundle should stay stage-oriented while still loading proposal, stakeholder, and report fields.

**Scenario:**
A DAO plans to change treasury allocation from long-term ecosystem grants to short-term growth campaigns. Stakeholders include core contributors, token holders, external builders, and governance delegates.

**Expected questions:**
- Will short-term growth weaken long-term trust?
- Which stakeholders resist first?
- What messaging or safeguards reduce backlash?

---

If you need a compact replay note for one review-pack scenario that regenerates JSON, Markdown, and HTML artifacts under one basename, open `docs/SCENARIO_REVIEW_PACK_REPLAY_NOTE.md`.
If your review export nests the same payload under `scenario_review_pack` or `scenario_review_pack_bundle`, the scenario-file import path still resolves and can generate the same report bundle without reshaping the JSON/YAML first.
If you need a compact audience note that keeps one imported scenario tied to the reviewers who should open the generated bundle first, open `docs/SCENARIO_REPORT_REVIEWER_AUDIENCE_NOTE.md`.
If your imported bundle already exposes the source as `scenario_src` or `source_href`, the same scenario-file report flow still carries that scenario source path or URL into the generated report bundle metadata.
If your export keeps the same value under `source_location`, the CLI resolves it into the same report metadata without reshaping the scenario file first.
If you need the matching short note, open `docs/SCENARIO_SOURCE_LOCATION_ALIAS_NOTE.md`.
If you need the matching short-alias note, open `docs/SCENARIO_SOURCE_SHORT_ALIASES_NOTE.md`.
If you want one source-first note that keeps the imported scenario file tied to its shared report bundle, open `docs/GOVERNANCE_SANDBOX_SCENARIO_SOURCE_BUNDLE_NOTE.md`.
If you want a YAML-first rehearsal fixture that proves the same scenario-file import path plus markdown/html/json outputs, open `examples/delegate-ready-rehearsal.yaml`.
If you need the matching wrapper note for workshop exports that arrive as `scenario_storyboard`, open `docs/SCENARIO_STORYBOARD_NOTE.md`.
If your workshop export nests the same payload under `scenario_storyboard_bundle`, the same scenario-file import path still resolves and can generate the same report bundle without reshaping the file first.
If your workshop export nests the same payload under `scenario_workshop` or `scenario_workshop_bundle`, the scenario-file import path still resolves and can generate the same report bundle without reshaping the file first.
If you need a compact note for staged scenario-file wrappers before widening preset or demo scope, open `docs/SCENARIO_STAGE_WRAPPER_NOTE.md`.
If your review export nests the same payload under `scenario_report_bundle` or `scenario_report_bundle_pack`, the scenario-file import path still resolves and can regenerate the same report bundle without reshaping the JSON/YAML first.
If your workbench export nests the same payload under `scenario_workbench` or `scenario_workbench_bundle`, the same scenario-file import path still resolves and can generate the same report bundle without reshaping the JSON/YAML first.
If your workflow export nests the same payload under `scenario_workflow` or `scenario_workflow_bundle`, the same scenario-file import path still resolves and can generate the same report bundle without reshaping the JSON/YAML first.
If your design-studio export nests the same payload under `scenario_studio` or `scenario_studio_bundle`, the same scenario-file import path still resolves and can generate the same report bundle without reshaping the JSON/YAML first.

## Quickstart

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --proposal "Shift 25% of treasury budget from grants to growth campaigns" \
  --stakeholders "core contributors,token holders,external builders,governance delegates"
```

Or generate the default report bundle in one step:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario.yaml \
  --report-dir artifacts/demo
```

Use the richer scenario/report fixture when you want one YAML file to drive proposal input, stakeholder presets, report naming, and a reusable JSON/Markdown/HTML artifact bundle:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-report-bundle.yaml \
  --report-dir artifacts/delegate-ready
```

For the shortest replayable scenario-file -> report-bundle workflow, open `docs/SCENARIO_REPORT_QUICKSTART.md`.
If you want a one-screen start note for the same scenario-file + report-dir bundle, open `docs/SCENARIO_REPORT_START.md`.
If you need a compact path check for one imported scenario file plus one generated report bundle, open `docs/SCENARIO_REPORT_PATHS_NOTE.md`.
If you need the shortest top-level alias for the report bundle directory, open `docs/REPORT_FOLDER_ALIAS_NOTE.md`.
Plural directory aliases like `reports_dir`, `reports_directory`, and `reports_folder` also work when a scenario fixture needs report-bundle wording that matches an export form or reviewer handoff.
If you want a JSON-first fixture that proves one imported scenario can generate a named markdown/html/json report bundle, open `examples/scenario-markdown-report.json`.
If you need a compact note for keeping the markdown report paired with the matching JSON artifact, open `docs/SCENARIO_REPORT_MARKDOWN_BUNDLE_NOTE.md`.
If you need a compact replay note focused on regenerating Markdown and HTML from the same imported scenario file, open `docs/SCENARIO_FILE_REPORT_MARKDOWN_HTML_REPLAY_NOTE.md`.
If you need the shortest reviewer-first cue for reopening one imported scenario with its shared JSON/Markdown/HTML outputs, open `docs/SCENARIO_REPORT_REVIEW_BUNDLE_START.md`.
If you want the same bundle flow with a ready-made JSON fixture, start with `examples/scenario-report-bundle.json`.
If you want a YAML fixture that keeps a singular `report.reviewer` alias tied to the generated markdown/html/json bundle, start with `examples/scenario-report-reviewer.yaml`.
If you want a reviewer-focused YAML fixture with the same alias flow plus a named report bundle, start with `examples/scenario-report-reviewers.yaml`.
If you want the same flow from stdin for shell pipelines or browser-demo handoffs, pass `--scenario-file -` and pipe JSON/YAML into the CLI.
Scenario files can also keep `stakeholders` as one comma-separated or newline-separated string when a fixture is easier to author that way.
Scenario files can also use `proposal_outline`, `proposal_notes`, or `proposal_details` when workshop exports keep the proposal object under a named planning block.
Individual stakeholder entries can also use `participant`, `actor`, or `faction` as name aliases when scenario files come from demo-form or workshop exports.
Stakeholder preset maps can also use `bloc` as a compact alias for the built-in preset key when scenario fixtures are authored for governance workshops.
If you want one fixture to keep proposal/stakeholders under `inputs` and report metadata under `inputs.report`, open `docs/GOVERNANCE_SANDBOX_SCENARIO_INPUTS_REPORT_NOTE.md`.
If you need a compact note for root-style report directory aliases in scenario bundles, open `docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_ROOT_ALIAS_NOTE.md`.
If you need a compact note for the plural `reports_directory` alias before widening presets or web-demo scope, open `docs/SCENARIO_REPORTS_DIRECTORY_ALIAS_NOTE.md`.
If you need the matching short status cue for that same `reports_directory` replay lane, open `docs/SCENARIO_REPORTS_DIRECTORY_STATUS_NOTE.md`.
If your scenario file already describes the shared report bundle as an artifacts directory, the same report flow now accepts `artifact_dir`, `artifacts_dir`, or `artifacts_directory` under `report.outputs`; see `docs/REPORT_ARTIFACTS_DIRECTORY_ALIAS_NOTE.md`.
Scenario files can also use top-level `report_downloads` when one imported rehearsal should regenerate download-oriented JSON/Markdown/HTML report files without reshaping the fixture first.
If you need a compact note for that download-oriented alias, open `docs/REPORT_DOWNLOADS_ALIAS_NOTE.md`.
If you need a compact note for the `report_directory` alias before widening report-bundle wiring, open `docs/GOVERNANCE_SANDBOX_REPORT_DIRECTORY_ALIAS_NOTE.md`.
If you want a demo-oriented fixture for the first web form plus report-card flow, start with `examples/scenario-web-demo.yaml`.
If you need a compact UI boundary note before widening that first form-to-card slice, open `docs/WEB_DEMO_FORM_TO_CARD_SCOPE.md`.
If you need a compact acceptance note for when that first result card plus report path is actually reviewable, open `docs/WEB_DEMO_RESULT_CARD_ACCEPTANCE.md`.
If you need a one-line maintainer update once that first result-card proof is believable, open `docs/WEB_DEMO_RESULT_CARD_STATUS_LINE.md`.
If you need a compact phase-one checklist that keeps scenario-file input and the report bundle ahead of presets, web demo work, and the demo GIF, open `docs/SCENARIO_FILE_REPORT_PHASE_ONE_CHECKLIST.md`.
If you need a compact phase-one reminder to keep scenario-file import and markdown/html/json report output as the release gate before presets or web demo work, open `docs/SCENARIO_FILE_REPORT_PHASE_ONE_GATE_NOTE.md`.
If you need a compact phase-one reminder to keep one scenario-file replay tied to one validated JSON/Markdown/HTML report bundle, open `docs/SCENARIO_FILE_REPORT_VALIDATE_GATE.md`.
If you need a compact stage gate for keeping one scenario-file replay tied to one regenerated JSON/Markdown/HTML report bundle before widening presets or demo scope, open `docs/SCENARIO_FILE_REPORT_STAGE_GATE.md`.

If you need a compact phase-one reminder to validate one scenario-file plus one regenerated markdown/html/json report bundle before push, open `docs/SCENARIO_FILE_REPORT_VALIDATE_SMALL_SLICE_NOTE.md`.
If you need the matching compact reminder to keep one scenario-file replay tied to one short artifact-path status line, open `docs/SCENARIO_FILE_REPORT_INDEX_CARD_NOTE.md`.
If you need a compact repo-4/repo-5 status reminder for that same five-repo loop, open `docs/SCENARIO_FILE_REPORT_REPO45_STATUS_NOTE.md`.
If you need a compact phase-one recheck before widening presets or demo scope, open `docs/SCENARIO_FILE_REPORT_RECHECK_NOTE.md` to replay one scenario file against the regenerated JSON/Markdown/HTML bundle.
If you want a ready-made JSON scenario that keeps preset-backed stakeholders plus owner/audience report metadata in the same phase-one replay lane, open `examples/scenario-phase-one-owner-audience.json`.
If you need a compact phase-one reminder to keep report-path validation tied to the same scenario-file input before widening preset or demo scope, open `docs/SCENARIO_FILE_REPORT_PATH_LOCK_NOTE.md`.
If you need a compact replay note for one scenario file plus one named report directory handoff before widening presets or web demo scope, open `docs/SCENARIO_FILE_REPORT_DIR_HANDOFF_NOTE.md`.
If you want the shortest UI/UX handoff note before widening the first web demo, open `docs/GOVERNANCE_SANDBOX_UI_UX_PRO_MAX_BRIDGE.md`.
If you need a compact PM-facing rule for keeping scenario-file import, markdown/html/json report output, and the first web-demo checkpoint aligned, open `docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_WEB_DEMO_BRIDGE.md`.
If you need the matching Playwright-style stability note before widening that first form-to-result-card demo, open `docs/WEB_DEMO_PLAYWRIGHT_STABILITY_NOTE.md`.
If you need a compact phase-one gate that keeps scenario-file report generation ahead of demo polish while preserving UI/UX and Playwright-style replay discipline, open `docs/SCENARIO_FILE_REPORT_UI_PLAYWRIGHT_GATE.md`.
If you want a DAO-flavored treasury automation rehearsal with presets plus a named report bundle, start with `examples/dao-treasury-automation.yaml`.
If you want a broader preset mix that highlights community-trust tradeoffs plus a named memo bundle, start with `examples/scenario-community-feedback.yaml`.
If you want one reviewer-ready YAML fixture that keeps scenario import, named markdown/html/json outputs, audience, and owner metadata together, start with `examples/scenario-review-pack.yaml`.
If you want one reusable fixture that exercises all built-in stakeholder presets in a single report bundle, start with `examples/scenario-preset-roundtable.yaml`.
If you want the most compact catalog fixture for replaying dao/delegates/contributors/investors/community together, start with `examples/scenario-stakeholder-preset-catalog.yaml`.
If you want rehearsal-labeled exports to keep the same scenario-file import path, open `docs/SCENARIO_REHEARSAL_WRAPPER_NOTE.md`.
If your workshop export nests the same payload under `scenario_rehearsal_bundle`, the scenario-file import path still resolves without reshaping the JSON/YAML first.
If your workshop export nests the same payload under `scenario_session_bundle`, the scenario-file import path still resolves and can generate the same report bundle without reshaping the JSON/YAML first.
If your workshop export nests the fixture under `scenario_manifest_bundle` or `scenario_packet_bundle`, the same scenario-file import path still resolves and can generate the report bundle without reshaping the file first.
If you want a compact snake_case basename fixture for scenario-file -> report-bundle replay, start with `examples/scenario-base-name-alias.yaml` or `examples/scenario-base-name-alias.json`.
If you want the same scenario-file flow as a compact DAO-oriented JSON fixture, start with `examples/scenario-dao-report-bundle.json`.
CLI-provided relative `--report-json`, `--report-markdown`, and `--report-html` paths now resolve from the scenario-file directory, so replayable fixtures can keep outputs beside the imported scenario without shell-specific path glue.
If you need a compact replay note for that same relative-path report flow before widening the web demo, open `docs/SCENARIO_REPORT_RELATIVE_PATH_REPLAY.md`.
If you need a machine-readable preset inventory for scenario generators or web-demo forms, run `PYTHONPATH=src python3 -m governance_sandbox.cli run --list-presets-json`.
If you need the shortest UI handoff for turning that preset JSON into the first scenario form plus result card, open `docs/PRESET_JSON_FORM_CARD_START.md`.
That preset-aware report flow now keeps a short preset summary beside each known preset in markdown/html stakeholder sections, so memo readers can see the trait meaning without reopening preset docs.
If you want a tiny scenario-file fixture that demonstrates top-level `report_targets` + `report_tags` aliases, start with `examples/scenario-report-targets-alias.yaml`.
If you need a compact note for `priority_level` or `priority_label` aliases before widening scenario-import fixtures, open `docs/SCENARIO_REPORT_PRIORITY_LEVEL_ALIAS_NOTE.md`.
If you need the same report-priority lane through `priority_lane` or `urgency_label` aliases, open `docs/SCENARIO_REPORT_PRIORITY_LANE_NOTE.md`.
If you want a compact scenario-file alias for report triage wording, `priority_band` now resolves to the same report priority field in JSON/Markdown/HTML outputs.
If you want one nested `inputs.report.outputs` fixture that keeps proposal input, stakeholder presets, and bundle basename together, start with `examples/scenario-inputs-report-outputs.yaml`.

That JSON inventory now includes a label and a short summary for each preset so scenario builders and UI forms can explain the trait choice without hard-coding copy.
Scenario files can also carry `report.audience` / `report.audiences` (or top-level `report_audience`, `report_audiences`, `report_readers`, `report_targets`, `audience`, or `audiences`) so markdown/html outputs state who the memo is for without duplicating handoff copy outside the fixture.
Scenario files can also carry `report.subtitle` / `report.subheading` (or top-level `report_subtitle`) so markdown/html outputs can keep one reviewer-facing subtitle under the main memo title.
Scenario files can also carry `report.subject` / `report.subjects` (or top-level `report_subject`, `report_subjects`, `subject`, `subjects`, `topic`, or `topics`) so generated report bundles keep one explicit memo subject beside the title and audience metadata.
Scenario files can now also carry `report.owner` / `report.owners` (or top-level `report_owner`, `report_owners`, `owner`, or `owners`) so markdown/html outputs keep the maintainer handoff visible beside the audience metadata.
Scenario files can also use `report.goal` / `report.goals` / `report.purpose` (or top-level `report_goal`) when one imported rehearsal pack should carry a reviewer-facing memo summary into markdown/html outputs without renaming existing workshop fields.
Scenario files can now also carry `report.priority` / `report.urgency` (or top-level `report_priority`, `report_urgency`, `priority`, or `urgency`) so markdown/html outputs keep one reviewer-facing priority lane visible beside the subject and owner metadata.
If you need a compact reminder for keeping one report subject visible across scenario-file, markdown, and HTML outputs, open `docs/SCENARIO_REPORT_SUBJECT_NOTE.md`.
If you need a compact reminder for scenario files that keep report subject, owner, and audience bundled across JSON, Markdown, and HTML outputs, open `docs/SCENARIO_REPORT_TRIAGE_NOTE.md`.
If you need the fastest scenario-file -> rendered-audience proof before wider report-bundle or web-demo work, open `docs/SCENARIO_REPORT_AUDIENCE_START.md`.
If you need a compact reminder that scenario tags should stay visible in the generated report panel as well as the source fixture, open `docs/SCENARIO_REPORT_TAGS_NOTE.md`.
If you need a compact handoff note for keeping scenario-file audience and owner metadata visible together in one generated report bundle, open `docs/SCENARIO_REPORT_OWNER_AUDIENCE_HANDOFF.md`.
If you need the narrowest start for that same owner+audience replay lane, open `docs/SCENARIO_FILE_REPORT_OWNER_AUDIENCE_START.md`.
If you need a compact PM start for scenario files that should surface report owner and audience in the first markdown/html/json bundle, open `docs/GOVERNANCE_SANDBOX_SCENARIO_FILE_REPORT_OWNER_AUDIENCE_START.md`.
If you need the shortest metadata-first replay before widening scenario bundles or the first web demo, open `docs/SCENARIO_REPORT_METADATA_START.md`.
If you need the shortest scenario-file-first reminder before proving markdown/html export with preset-backed stakeholders, open `docs/SCENARIO_PRESET_REPORT_START.md`.
If you need one scenario file to produce a title-ready report bundle for humans without reopening the JSON first, start with `examples/scenario-community-feedback.yaml`.
If you need a compact start note for keeping one scenario replay tied to one reusable JSON/Markdown/HTML artifact bundle, open `docs/SCENARIO_REPORT_ARTIFACT_BUNDLE_START.md`.
If you need the shortest scenario-file -> generated report bundle replay before widening scope, open `docs/SCENARIO_FILE_REPORT_START.md`.
If you need a compact reminder to keep JSON/YAML scenario import coupled to the generated report trio, open `docs/SCENARIO_FILE_JSON_YAML_REPORT_START.md`.
If you need the matching replay reminder for `.yml` fixtures that should produce the same JSON/Markdown/HTML report bundle as `.yaml`, open `docs/SCENARIO_FILE_YML_REPORT_REPLAY_NOTE.md`.
If you need a compact stack note for keeping one imported scenario tied to JSON, Markdown, and HTML outputs together, open `docs/SCENARIO_FILE_REPORT_MARKDOWN_HTML_STACK.md`.
If you need a compact reminder that relative report paths inside a scenario file resolve from that scenario file's directory, open `docs/SCENARIO_FILE_RELATIVE_REPORT_PATHS_NOTE.md`.
If you need a compact reminder that top-level `report_markdown_output` can point straight at the generated memo file, open `docs/SCENARIO_FILE_REPORT_MARKDOWN_OUTPUT_ALIAS_NOTE.md`.
Top-level scenario fixtures now also accept `output_md_path` / `output_md_file` when one imported JSON or YAML scenario should point directly at the generated Markdown report path.
If you need a compact reminder that `report.output_file_stem` and top-level `report_output_file_stem` can drive the same generated markdown/html/json bundle basename, open `docs/SCENARIO_REPORT_OUTPUT_FILE_STEM_ALIAS_NOTE.md`.
If you need a compact reminder for carrying one scenario-file `report.description` into the generated markdown/html memo bundle, open `docs/SCENARIO_FILE_REPORT_DESCRIPTION_NOTE.md`.
If you need a compact reminder that scenario-file support and markdown/html report generation stay first in the build order, open `docs/SCENARIO_FILE_REPORT_PRIORITY.md`.
If you need a one-screen reminder that JSON/YAML scenario-file input plus regenerated JSON/Markdown/HTML reports is still the current minimum believable slice, open `docs/SCENARIO_FILE_REPORT_JSON_YAML_PRIORITY_NOTE.md`.
If you need a compact phase-one reminder to keep one imported scenario fixture tied to its regenerated markdown/html/json report trio and visible basename before widening presets or web-demo scope, open `docs/SCENARIO_FILE_REPORT_FIXTURE_TRIO_NOTE.md`.
If you need a compact phase-one reminder to keep scenario-file + markdown/html report work ahead of presets and web-demo scope in the same delivery ladder, open `docs/SCENARIO_FILE_REPORT_DELIVERY_LADDER_NOTE.md`.
If you need a compact recheck before widening beyond scenario-file/report work, open `docs/SCENARIO_FILE_REPORT_PRIORITY_RECHECK_NOTE.md`.
If you need a one-line status cue for the current phase-one slice, open `docs/SCENARIO_FILE_REPORT_PHASE_ONE_STATUS.md`.

If you want one reusable scenario fixture that keeps stakeholder presets and report subtitle metadata in the same scenario-file -> markdown/html/json proof lane, start with `examples/scenario-preset-subtitle-report.yaml`.
If you want a compact phase-one fixture for scenario-file input plus markdown/html/json report output, start with `examples/scenario-phase-one-report-stack.yaml`.

If you need a compact rule for keeping scenario-file examples tied to a named report basename before widening web-demo scope, open `docs/SCENARIO_FILE_REPORT_BASENAME_RULE.md`.
If you need a compact note for scenario fixtures wrapped under `scenario_plan` or `scenario_manifest`, open `docs/SCENARIO_MANIFEST_WRAPPER_NOTE.md`.
If you need the matching archive-style replay note for `scenario_archive`, open `docs/SCENARIO_ARCHIVE_WRAPPER_NOTE.md`.
If you want the same wrapper flow under `scenario_lab_bundle`, keep the imported scenario envelope and regenerate the same markdown/html/json report bundle.
If you want a cleaner scenario-file alias for proposal plus stakeholder imports, `scenario_playbook` now resolves through the same report bundle path.
If your workshop export nests the same payload under `scenario_playbook_bundle`, the scenario-file import path still resolves and can generate the same report bundle without reshaping the file first.
If you need the same wrapper flow under `scenario_packet`, open `docs/SCENARIO_PACKET_WRAPPER_NOTE.md`.
If you need a wrapper-based scenario fixture that still drives markdown/html/json report generation cleanly, start with `examples/scenario-rehearsal-wrapper.yaml`.
If you need the matching note for a plain top-level `scenario` wrapper before widening fixture reuse, open `docs/SCENARIO_TOP_LEVEL_WRAPPER_NOTE.md`.
If you need the matching note for `scenario_plan` wrappers before widening fixture reuse, open `docs/GOVERNANCE_SANDBOX_SCENARIO_PLAN_WRAPPER_NOTE.md`.
If you need the matching wrapper note for `scenario_blueprint` before widening scenario reuse, open `docs/SCENARIO_BLUEPRINT_WRAPPER_NOTE.md`.
If you need the matching wrapper note for `scenario_deck` before widening scenario-file/report reuse, open `docs/SCENARIO_DECK_WRAPPER_NOTE.md`.
If you need the matching wrapper note for `scenario_record` before widening scenario reuse, open `docs/SCENARIO_RECORD_WRAPPER_NOTE.md`.
If you need a compact reviewer-share note once one imported scenario already generates the full markdown/html/json bundle, open `docs/SCENARIO_REPORT_REVIEWER_SHARE_NOTE.md`.
If you need a compact handoff that keeps one scenario-file import tied to one report bundle plus visible owner/reviewer routing, open `docs/SCENARIO_FILE_REPORT_OWNER_REVIEWERS_NOTE.md
If you need the narrowest owner+review route for one scenario-file report bundle, open `docs/SCENARIO_FILE_REPORT_OWNER_REVIEW_ROUTE_NOTE.md`.
`.
If you need the shortest scenario-file -> markdown memo proof before widening JSON/HTML output work, open `docs/SCENARIO_FILE_MARKDOWN_REPORT_NOTE.md`.
If you need a compact PM-facing reminder to keep scenario input, report basename, and generated markdown/html/json output paths visible in one replay status line, open `docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_OUTPUT_PATH_STATUS_NOTE.md`.
If you need a compact replay card for keeping one imported scenario tied to one generated JSON/Markdown/HTML bundle, open `docs/SCENARIO_FILE_REPORT_REPLAY_CARD.md`.
If you need a compact reviewer note for checking the same imported scenario against the generated JSON/Markdown/HTML bundle, open `docs/SCENARIO_REPORT_OUTPUT_REVIEW_NOTE.md`.
If you need a compact reminder for keeping those same output paths grouped under one `report.outputs.files` mapping, open `docs/SCENARIO_REPORT_OUTPUT_FILES_NOTE.md`.
If you want a download-oriented alias for that same web-demo-friendly report bundle mapping, open `docs/SCENARIO_REPORT_DOWNLOADS_ALIAS_NOTE.md`.
If you want a ready-made JSON fixture for that same `report.outputs.files` mapping, start with `examples/scenario-report-output-files.json`.
If you need a one-line progress cue that names the imported scenario file plus generated review bundle status together, open `docs/SCENARIO_FILE_REPORT_STATUS_NOTE.md`.
If you need a compact PM-facing reminder to keep one imported scenario file tied to the generated JSON/Markdown/HTML output paths in the same replay status line, open `docs/SCENARIO_FILE_REPORT_OUTPUT_PATH_STATUS_NOTE.md`.
If you need a compact phase-one note for proving one imported scenario file plus one generated markdown/html/json report bundle before widening presets or demo scope, open `docs/SCENARIO_FILE_REPORT_VALIDATE_BUNDLE_NOTE.md`.
If you need a compact reminder to keep one fresh scenario-file/report-bundle win visible in the same pass as repo 4, open `docs/SCENARIO_FILE_REPORT_PROGRESS_SYNC_NOTE.md`.


If you need a one-line check that the imported scenario already produced the full report stack, open `docs/SCENARIO_REPORT_STACK_CHECK.md`.
If you need the narrowest scenario-file -> result card -> report-download start note before widening the first web demo, open `docs/SCENARIO_REPORT_RESULT_CARD_START.md`.
If you need a tiny download signoff note once that first web demo is already believable, open `docs/GOVERNANCE_SANDBOX_WEB_DEMO_DOWNLOAD_SIGNOFF.md`.
If you need the shortest stdin-first replay from one imported scenario payload to one generated report bundle, open `docs/SCENARIO_STDIN_REPORT_BUNDLE_START.md`.

---

## Why this project exists

Most governance tooling focuses on voting, execution, or on-chain recordkeeping.
Much less attention is given to **pre-decision rehearsal**:

- What happens if this proposal is misunderstood?
- Which stakeholders align or oppose it first?
- Which mitigation language should appear before launch?
- What second-order narrative risks are visible early?

This project exists to fill that gap.

---

## Product direction

This repository is intended to become a long-lived public simulation layer for governance teams, DAOs, policy groups, and agent-native decision systems.

### Direction 1 — Decision support over prediction theater
We do not aim to "predict everything." We aim to improve the quality of governance decisions by making reactions and tradeoffs easier to inspect.

### Direction 2 — Scenario clarity over model complexity
A smaller, auditable system with explicit assumptions is more useful than a flashy black box.

### Direction 3 — Governance-native workflows
Outputs should resemble real decision artifacts:

- stakeholder map
- alignment/conflict matrix
- risk summary
- mitigation recommendations
- final decision memo

### Direction 4 — Demo-ready public repos
Every release should improve the public-repo surface:

- cleaner README
- stronger visual walkthroughs
- scenario examples
- reproducible commands
- evidence of practical use

### Direction 5 — Extensible domain packs
Long term, this engine can support multiple domain packs:

- DAO governance
- public sentiment rehearsal
- internal org decision rehearsal
- policy and communications scenarios

---

## MVP scope

Current MVP includes:

- proposal input
- stakeholder list input
- simple heuristic response simulation
- structured decision memo output

Near-term additions:

- richer stakeholder traits and scenario presets
- conflict graph export
- lightweight web demo for replayable proposal input and result cards
- demo GIF once the first web flow is stable

Current CLI additions now include:

- optional scenario metadata (`name`, `context` / `decision_context`) loaded from scenario files and surfaced in reports
- `--scenario-file` for JSON/YAML proposal + stakeholder input
- nested scenario blocks (`scenario.name`, `scenario.context`, `inputs.proposal`, `inputs.stakeholders`) for reusable demo fixtures and UI handoff payloads
- scenario-file aliases for lightweight imports (`title` → scenario name, `decision`/`summary` → report context, `proposal_text`/`prompt` → proposal, `participants`/`actors` → stakeholders, stakeholder `preset_name`/`preset_key`/`group`/`trait`/`segment`/`cohort`/`role` → preset, `preset_groups`/`stakeholder_preset_map` → stakeholder preset map)
- `--report-markdown` for a local decision memo report file
- `--report-html` for a lightweight visual report artifact
- `--report-json` for writing the structured output artifact to disk
- `--report-dir` for emitting a default report artifact bundle in one command
- scenario-file `report.json_path` / `report.markdown_path` / `report.html_path` aliases for fixture-driven output paths without repeating CLI flags
- top-level `report_json_path` / `report_markdown_path` / `report_html_path` aliases for scenario files that want output paths without nesting a `report` block
- top-level `scenario_payload` / `scenario_data` / `scenario_bundle` / `scenario_document` / `scenario_spec` / `scenario_deck` wrappers for exported JSON/YAML fixtures that keep the reusable scenario under one extra envelope
- `docs/README_SCENARIO_WRAPPER_ALIAS_NOTE.md` for the shortest wrapper-first authoring reminder before widening report or web-demo work
- `docs/SCENARIO_INPUTS_WRAPPER_ALIAS_NOTE.md` for the matching plural-wrapper reminder when fixtures keep proposal, stakeholders, and report metadata under `scenario_inputs`
- scenario `tags` / `labels` for reusable demo fixtures and richer markdown/html report context
- optional scenario `report_title` / `report_heading` metadata for cleaner markdown/html memo headings, page titles, and demo handoff bundles
- nested `report.title` / `report.heading`, `report.tags`, and `report.description` blocks for report-first scenario fixtures and UI handoff payloads
- `report.name` as a scenario-file alias for the default report bundle basename when `--report-dir` is used
- `report.base_name` as a scenario-file alias when existing fixtures already use snake_case basename fields
- `report.file_stem` / `report.stem` as scenario-file aliases when the bundle should keep one reusable basename across JSON/Markdown/HTML artifacts
- `report.slug` as a scenario-file alias when fixtures want one compact, URL-safe basename for the generated report bundle
- `report.output_basename`, `report.output_name`, and top-level `report_basename` / `report_file_stem` / `report_stem` / `report_name` aliases for reviewer-ready report bundle basenames
- `report.output_name`, `report.report_name`, and top-level `report_file_stem` / `report_name` aliases for reviewer-ready report file naming cues (`docs/SCENARIO_REPORT_FILE_ALIAS_NOTE.md`)
- `report.description` feeds the generated markdown/html report summary so one scenario file can carry reviewer-facing memo context into CLI and web-demo handoffs
- `report.memo_summary` / `report.executive_summary` / `report.overview` / `report.memo` as summary aliases for scenario files that already carry memo-oriented report metadata
- `report.report_summary` as a nested scenario-file alias when UI/demo payloads already name the memo summary explicitly
- scenario `description` as a lightweight context alias for report-oriented fixtures
- outcome snapshot summaries in JSON + markdown/html reports so stakeholder stance balance is visible at a glance
- `run --list-presets` for built-in stakeholder trait groups (`dao`, `delegates`, `contributors`, `investors`, `community`)

---

## Repository structure

```text
governance-sandbox/
├─ README.md
├─ pyproject.toml
├─ src/governance_sandbox/
│  ├─ __init__.py
│  ├─ engine.py
│  └─ cli.py
├─ docs/assets/
│  ├─ screenshot-1.svg
│  ├─ screenshot-2.svg
│  └─ screenshot-3.svg
└─ .github/workflows/ci.yml
```

---

## Roadmap

### Phase 1
- MVP simulation engine
- CLI workflow
- launch-page style README

### Phase 2
- scenario file support
- markdown/html report generation
- richer stakeholder trait presets

### Phase 3
- domain packs
- visual stakeholder graph
- benchmark scenarios and replay comparison

### Phase 4
- browser UI
- saved simulation runs
- team workflow integration

---

## License

MIT


## Scenario-driven report bundles

Scenario files can now steer report bundle naming through `report.basename`, which is useful when you want stable markdown/html/json artifact names per rehearsal.
Configured `report.basename` values are sanitized into a safe slug so punctuation or path-like separators do not leak into the generated bundle paths.

```yaml
scenario:
  name: Treasury signal rehearsal
report:
  title: Delegate-ready rehearsal memo
  basename: delegate-ready-rehearsal
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
```

Then run `gov-sandbox run --scenario-file scenario.yaml --report-dir artifacts/` to produce `delegate-ready-rehearsal.json`, `.md`, and `.html`.
If `report.basename` is omitted, `report.title` becomes the default bundle basename before the CLI falls back to generic `report.*` filenames.

Scenario maps can now use nested stakeholder objects with alias fields like `label`/`title` plus `trait_preset`, which keeps JSON/YAML scenario files readable while still producing the same preset-backed report outputs.

Scenario files may also use `report.bundle_dir`, nested `report.report_dir`, or top-level `report_output_dir` aliases when one scenario fixture should own the entire JSON/markdown/HTML bundle directory without repeating CLI flags.
Scenario files may also use `report.root` or `report.report_root` when a fixture wants one short output-root alias for the generated report bundle.

Scenario files may also use `report_author` or `report_authors` as report-owner aliases when the generated markdown/html memo should show the owning working group without renaming existing fixture fields.

If you want a compact quickstart for one scenario file plus one shared JSON/Markdown/HTML bundle, open `docs/SCENARIO_REPORT_BUNDLE_QUICKSTART.md`.
If you want a compact source-provenance reminder before handing off a generated scenario report bundle, open `docs/SCENARIO_REPORT_SOURCE_HANDOFF.md`.
If you need a short alias reminder for keeping `scenario_source` / `source_path` metadata visible in stdin-generated markdown/html bundles, open `docs/SCENARIO_SOURCE_ALIAS_NOTE.md`.
If you need a compact reminder that `scenario_path` and `source_path` can preserve scenario-file provenance in saved reports, open `docs/GOVERNANCE_SANDBOX_SCENARIO_SOURCE_PATH_ALIAS_NOTE.md`.

If you need a compact CLI reminder for the shorter `--report-md` / `--report-htm` scenario replay path, open `docs/SCENARIO_REPORT_SHORT_FLAG_NOTE.md`.

If you need a compact reminder that governance-sandbox still ships in the order scenario file -> report bundle -> presets -> web demo -> demo GIF, open `docs/SCENARIO_REPORT_PRIORITY_LADDER_NOTE.md`.

If you need a compact note for scenario files that export the proposal under `proposal_body` while keeping the same report flow, open `docs/GOVERNANCE_SANDBOX_PROPOSAL_BODY_ALIAS_NOTE.md`.

If you need a compact note for `report.watchers` or `report_watchers` while keeping the same markdown/html/json memo audience output, open `docs/SCENARIO_REPORT_WATCHERS_ALIAS_NOTE.md`.
If you need a compact note for reusing one scenario-file handoff sentence as the generated report summary via `report_follow_up`, open `docs/SCENARIO_REPORT_FOLLOW_UP_ALIAS_NOTE.md`.
If you need the same summary shortcut under `report_takeaway` / `takeaway`, open `docs/SCENARIO_REPORT_TAKEAWAY_ALIAS_NOTE.md`.
If you need a compact note for the more explicit `report.outputs.bundle_basename` alias before widening scenario bundle naming rules, open `docs/SCENARIO_REPORT_BUNDLE_BASENAME_ALIAS_NOTE.md`.
If you need a compact alias note for driving that same governance-sandbox report bundle from `report.output_slug` or `report.outputs.output_slug`, open `docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_SLUG_ALIAS_NOTE.md`.
If you need a compact phase-one reminder that scenario-file replay should keep the same visible output slug across JSON, Markdown, and HTML artifacts, open `docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_OUTPUT_SLUG_NOTE.md`.
If you need the matching alias note for reviewer-facing `report.output_label` bundle naming, open `docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_LABEL_ALIAS_NOTE.md`.

If you need the matching PM note for `scenario_archive` wrappers that should still replay one JSON/Markdown/HTML report stack, open `docs/SCENARIO_ARCHIVE_REPORT_STACK_NOTE.md`.

If you need the short-form `json_report` / `markdown_report` / `html_report` names inside `report.outputs.files`, open `docs/GOVERNANCE_SANDBOX_REPORT_OUTPUT_FILES_SHORT_ALIASES_NOTE.md`.

If you need a compact replay note for keeping one imported scenario file tied to one reviewable markdown/html/json bundle, open `docs/SCENARIO_FILE_REPORT_REVIEW_STACK_NOTE.md`.

If you need a compact owner-facing note for keeping one scenario file tied to one markdown/html/json report bundle plus one generated-artifact summary line, open `docs/SCENARIO_FILE_REPORT_OWNER_SUMMARY_NOTE.md`.

If you need a quick wording cue for `report.digest` in generated markdown/html/json bundles, open `docs/GOVERNANCE_SANDBOX_REPORT_DIGEST_ALIAS_NOTE.md`.

If you need a compact owner-facing note for keeping one stdin-capable scenario replay tied to one JSON/Markdown/HTML report bundle plus a visible source/output status line, open `docs/GOVERNANCE_SANDBOX_SCENARIO_STDIN_REPORT_OWNER_NOTE.md`.

If you need a compact PM recheck for keeping one imported scenario file tied to one regenerated JSON/Markdown/HTML bundle before widening presets or demo work, open `docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_PHASE_ONE_RECHECK.md`.

If you need the shortest owner-facing status note for keeping one imported scenario file tied to one generated markdown/html/json report bundle, open `docs/SCENARIO_FILE_REPORT_OWNER_STATUS_NOTE.md`.

If you need a compact note for the top-level `report_markdown_target` / `report_html_target` aliases before widening scenario-file fixtures, open `docs/SCENARIO_REPORT_TARGET_ALIAS_NOTE.md`.
If you need a compact phase-one recheck note for keeping one imported scenario file tied to one regenerated JSON/Markdown/HTML report bundle before wider preset or web-demo work, open `docs/GOVERNANCE_SANDBOX_SCENARIO_REPORT_PHASE_ONE_RECHECK_NOTE.md`.
