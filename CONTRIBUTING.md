# Contributing and release validation

This guide is for contributors changing mcp-sauna and maintainers validating a release. **It is not needed to install or use the skill.**

## Local checks

Prerequisites: Node.js 22+ and Python 3.10+. The skill itself has no installation dependencies; Python is only used by the optional local grader and project checks.

```sh
npm ci
npm test
npm audit --audit-level=high
```

## Reference-server evaluation

The local MCP servers use synthetic wholesale-company data and run over stdio. They are unrelated to AgentFinland and do not connect to external systems. Writes are disabled by default; `SAUNA_ALLOW_WRITES=1` enables only the good server's synthetic in-memory `place_order` tool.

Configure an MCP client to run `node reference-servers/server.mjs` with `SAUNA_VARIANT=naive` or `SAUNA_VARIANT=good`. See `examples/mcp-config.example.json` and use `examples/tasks.example.yaml` for confirmed tasks. Run the skill against each server, save the sanitized reports, then check seeded findings and repeatability:

```sh
python3 scripts/check_reference_eval.py naive results-naive.json
python3 scripts/check_reference_eval.py good results-good.json
python3 scripts/grade.py --compare results-naive-run1.json results-naive-run2.json
python3 scripts/grade.py --compare results-good-run1.json results-good-run2.json
```

The naive fixture expectations are in `eval/reference-expectations.json`. The good fixture should have no High or Critical findings. These scripts check structured rule IDs and grades; they do not interpret report prose.

## Cross-agent release checks

Testing in Claude Code, Codex, and GitHub Copilot verifies skill portability. This is release-maintainer work; an end user does not need to install or run multiple agents. Follow `eval/agent-matrix.md`, keep the shared skill unchanged between hosts, and record untested hosts honestly.

## Manually grade a saved run

The host agent normally invokes `grade.py` automatically when Python 3.10+ is available. Maintainers can run it directly to inspect or regrade a sanitized `run.json`:

```sh
python3 scripts/grade.py run.json --json-out results.json --markdown-out report.md
```

The script uses only the Python standard library, makes no network calls, and rejects raw argument/result values in call logs.

The report footer reads the booking link from `MCP_SAUNA_BOOKING_URL`. Set it to an HTTPS URL before publishing reports that should include the paid-review link.
