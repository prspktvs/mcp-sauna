# Cross-agent evaluation record

> Historical v0.1 evaluation only. These runs predate the stable v1.0.0 release and do not establish v1.0.0 host compatibility. The stable release does not claim complete cross-host parity.

The v0.1 portability criterion requires running the same skill files unchanged in Claude Code, Codex, and GitHub Copilot. Do not infer compatibility from a passing run in only one host.

## Result summary

| Host | Model | OS | Skill revision | Naive seeded findings | Good High/Critical false positives | Safety gates | Two-run stability | Full naive review | Artifacts |
| --- | --- | --- | --- | --- | ---: | --- | --- | ---: | --- |
| Codex CLI 0.166.0 | Not captured | macOS 26.5.2 | Base commit `8ec6b99` | Pass | 0 | Honored; no writes | Stable grade and High/Critical set | 108 sec | `eval/artifacts/codex-*` |
| Claude Code 2.1.319 | `claude-sonnet-5-5` | macOS 26.5.2 | Base `8ec6b99` plus the T5 checklist clarification recorded here | Pass | 0 | Honored; no writes | Stable grade and High/Critical set | 110 sec | `eval/artifacts/claude-*` |
| GitHub Copilot | — | — | — | Not tested | — | — | — | — | — |

The naive and good reference-server files used for these runs are unchanged from `8ec6b99`. Codex completed its two naive runs in 108 and 126 seconds and its good-server run in 110 seconds. Claude completed its two naive runs in 110 and 94 seconds and its good-server run in 67 seconds. Both hosts' naive runs had an incomplete overall grade because some probes were skipped; the repeatability check compares that grade and the High/Critical set, not whether every probe ran.

Claude's earlier run omitted one Medium T5 finding. The skill's T5 instruction was clarified to require a tool-by-identifier completeness check before the two recorded final-skill naive runs; both then reported all six affected tools and passed the fixture checker. Codex's saved artifacts predate that clarification, so exact cross-host parity on identical skill files has not yet been established. The evaluation date is 2026-11-09.

Run procedure:

1. Install the repository's root skill directory without modifying its content.
2. Connect either `reference-servers/server.mjs` with `SAUNA_VARIANT=naive` or `good`, using a test label.
3. Configure a second isolated process with `SAUNA_IDENTITY=B` when checking identity separation; the first uses `SAUNA_IDENTITY=A`.
4. Ask the host to run mcp-sauna, provide `examples/tasks.example.yaml`, and confirm the read task list. Do not enable write probes in a portability run.
5. Save sanitized `results.json`. Run the appropriate `check_reference_eval.py` command.
6. Repeat from a fresh conversation against the same server snapshot and compare results with `grade.py --compare`.
7. Review the complete sanitized findings. Record any host-specific changes; a portability pass requires no changes to `SKILL.md`, references, or scripts.

The initial release report must label any unrun host as **not tested**. Never claim three-agent compatibility before all three rows have evidence.

## Interpretation

Repeatability passed within Codex and Claude. Exact cross-host parity is not established because the saved Claude runs include the T5 checklist clarification that the Codex artifacts predate. GitHub Copilot is **not tested**, so v0.1 did not meet its three-agent criterion and that historical version remained a prerelease. This is not a fresh evaluation of v1.0.0.
