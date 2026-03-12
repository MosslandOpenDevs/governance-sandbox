# Scenario Packet Wrapper Note

Scenario files may wrap the reusable proposal + stakeholder payload under `scenario_packet`.

Use this alias when a form export or demo handoff wants one obvious envelope name but still needs the same JSON / Markdown / HTML report bundle path after import. Keep the wrapped payload shaped like the normal top-level scenario object so proposal, stakeholders, and report metadata still resolve in one pass.
