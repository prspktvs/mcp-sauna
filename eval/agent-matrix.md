# Cross-agent evaluation record

The v0.1 portability criterion requires running the same skill files unchanged in Claude Code, Codex, and GitHub Copilot. Do not infer compatibility from a passing run in only one host.

For each host, record:

| Field | Value |
| --- | --- |
| Host and version | |
| Model and version | |
| OS | |
| Skill source commit | |
| Naive reference server commit | |
| Good reference server commit | |
| Naive seeded findings all reported | |
| Good High/Critical false positives | |
| Safety gates honored | |
| Two-run grade/high-finding stability | |
| Full 20-tool naive review elapsed seconds | |
| Under 900 seconds | |
| Report artifact paths | |
| Reviewer/date | |

Run procedure:

1. Install the repository's root skill directory without modifying its content.
2. Connect either `reference-servers/server.mjs` with `SAUNA_VARIANT=naive` or `good`, using a test label.
3. Configure a second isolated process with `SAUNA_IDENTITY=B` when checking identity separation; the first uses `SAUNA_IDENTITY=A`.
4. Ask the host to run mcp-sauna, provide `examples/tasks.example.yaml`, and confirm the read task list. Do not enable write probes in a portability run.
5. Save sanitized `results.json`. Run the appropriate `check_reference_eval.py` command.
6. Repeat from a fresh conversation against the same server snapshot and compare results with `grade.py --compare`.
7. Review the complete sanitized findings. Record any host-specific changes; a portability pass requires no changes to `SKILL.md`, references, or scripts.

The initial release report must label any unrun host as **not tested**. Never claim three-agent compatibility before all three rows have evidence.

## Current local evidence

Codex CLI 0.166.0 completed two naive-server runs with all seeded findings present. `grade.py --compare` reported the same incomplete overall grade and identical High/Critical finding set. A good-server run had zero High/Critical false positives. All three Codex runs stayed under 900 seconds and made no write or destructive calls. The host did not expose MCP annotations, so the report includes one Medium S1 limitation.

Claude Code is **not tested** because the installed CLI was unauthenticated. GitHub Copilot is **not tested** because no local host/CLI was available. v0.1 has not met its three-agent release criterion; the published tag is therefore a prerelease.
