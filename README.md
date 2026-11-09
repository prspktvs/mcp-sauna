# mcp-sauna

**mcp-sauna** is an open-source Agent Skill for reviewing MCP server tool design and behavior. It guides a host agent through a cautious static review and bounded behavioral probes, then produces a prioritized scorecard. It does not edit the server.

This is a design review, not a security audit or MCP protocol conformance test. The skill asks for an explicit non-production environment before any probe and never calls destructive tools.

## Use the skill

Install the repository's root skill folder in the host's skills directory, or use `gh skill install prspktvs/mcp-sauna mcp-sauna` after publication when that GitHub CLI command is available. Otherwise clone the repository and copy its contents to the host's skill directory. Current project-level paths include:

- Claude Code: `.claude/skills/mcp-sauna/`
- Codex: `.agents/skills/mcp-sauna/`
- GitHub Copilot: `.github/skills/mcp-sauna/`

Keep the contents together so the skill can load `references/` and `scripts/`. Connect the MCP server as usual, start or point it at a `dev`, `test`, or `staging` environment, then ask the agent: “Put the `erp-test` MCP server through mcp-sauna.” The agent asks you to confirm drafted tasks and any write probes before using them.

The shared `SKILL.md` uses only Agent Skills standard frontmatter and Markdown. Host installation paths differ; the review instructions and supporting files do not.

## Run the local reference evaluation

The two reference servers use synthetic wholesale-company data. The naive reference has 20 tools, for the spec's full-review timing target. They are local MCP servers over stdio, unrelated to AgentFinland, and are not connected to external systems.

Reference writes are disabled by default. `SAUNA_ALLOW_WRITES=1` enables only the good reference server's synthetic in-memory `place_order` tool; never set it for a real MCP server.

```sh
npm ci
SAUNA_VARIANT=naive node reference-servers/server.mjs
```

Configure the host agent to start the command above as the `naive-demo` test server. For example, an MCP client configuration can set `command` to `node`, `args` to the absolute path of `reference-servers/server.mjs`, and `env` to `{"SAUNA_VARIANT":"naive"}`. Start the same server with `SAUNA_VARIANT=good` for the better-designed reference. Use `examples/tasks.example.yaml` for confirmed read tasks.

Run mcp-sauna against each server twice, save the sanitized `results.json` reports, then check seeded findings and repeatability:

```sh
python3 scripts/check_reference_eval.py naive results-naive.json
python3 scripts/check_reference_eval.py good results-good.json
python3 scripts/grade.py --compare results-naive-run1.json results-naive-run2.json
python3 scripts/grade.py --compare results-good-run1.json results-good-run2.json
```

The naive server is seeded with the findings in `eval/reference-expectations.json`. The good server should produce no High or Critical false positives. The checker evaluates rule IDs and tools; it does not reinterpret prose. `eval/agent-matrix.md` records the manual cross-agent procedure and evidence required for a release claim.

The current validation matrix and sanitized Codex artifacts are in `eval/agent-matrix-v0.1.json` and `eval/artifacts/`. Codex passed the naive seeded checks twice with stable high-severity findings and produced no High/Critical false positives on the good server. Claude Code and GitHub Copilot remain untested, so the three-agent release criterion is still open; this version is published as a prerelease.

## Grade a sanitized run

The skill may generate `run.json` using the schema in `references/report-template.md`. The standard-library grader validates structure, applies fixed rule severities, computes the scorecard, and emits equivalent JSON and Markdown reports:

```sh
python3 scripts/grade.py run.json --json-out results.json --markdown-out report.md
```

`grade.py` makes no network calls. It rejects raw call argument/result fields and derives severity from the stable rule table. The report contains identifiers and evidence references, not raw MCP data.

The report footer reads the paid-review booking link from `MCP_SAUNA_BOOKING_URL`. Set it to an HTTPS URL before publishing reports; without it, the report marks the link as unconfigured instead of inventing one.

## Safety and limitations

- Use only a test environment with synthetic or approved test data.
- Tool annotations are hints; the skill checks them against the published descriptions and observed behavior.
- Read-only probes are the default. Each write probe needs its own explicit confirmation, and destructive tools are never called.
- The report says that tool output passed through the model provider already used by the agent.
- The model decides whether findings are present; the script makes the grades repeatable once findings are structured. The judge is not an oracle. Audit sample reports manually.
- Identity testing requires two already-configured, non-production test connections with known different permissions.

## License

Apache-2.0. See [LICENSE](LICENSE).
