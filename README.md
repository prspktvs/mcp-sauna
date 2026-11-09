# mcp-sauna

**Give your MCP server a rehearsal before real users depend on it.**

Your agent never sees your backend. It sees tool names, descriptions, schemas, annotations, and the responses those tools return. That contract is the interface. If it is unclear, an agent can choose the wrong tool, guess at an ID, drown in search results, or mistake an error for “no matches”—even when every endpoint works.

mcp-sauna reviews that agent-facing experience and gives you a prioritized, evidence-backed report of what to fix.

> Connect your **development or test MCP server** to your agent, invoke the skill, and ask for a review. The agent runs it and produces the report. **You don’t run scripts, start test servers, or coordinate multiple agents.**

## Why use mcp-sauna?

Protocol checks can tell you that an MCP server responds. They cannot tell you whether an agent can use it to finish a real task.

An agent makes decisions from the tool contract: which operation fits, what an input means, whether a result is complete, and how to recover from an error. When that contract leaves gaps, the model has to guess. Users see the cost as failed requests, repeated calls, oversized answers, or a result that looks successful but is incomplete.

mcp-sauna helps you find those gaps while the server is still in development. It checks the interface the way an agent encounters it, then shows maintainers where to make the contract clearer and safer.

It is especially useful when you are:

- preparing an MCP server for agent or customer use;
- inheriting a server and need to understand its weak spots quickly;
- changing tools or schemas and want to catch regressions;
- comparing successive reviews to see whether fixes improved the experience.

If you are the only person calling a small internal MCP server, you may not need it yet. If an agent is part of your product, this is a practical check before users become the testers.

## What the review checks

The review looks for problems such as:

- two tools that look like they do the same job, with no guidance on which to choose;
- required inputs whose format or meaning is unclear;
- internal IDs the agent has no way to resolve;
- searches with no useful page boundary, or responses that return far more than a task needs;
- errors that leave the agent with no safe next step;
- state-changing tools whose safety annotations do not match what they do.

It also runs a bounded set of confirmed tasks through safe tools when the environment and tool contracts allow it. That helps reveal what static schema review misses: whether the workflow can complete, how errors behave, and how much context the results consume.

### Example finding

> **High — E1: Unhelpful error response** (`find_customer`, CALL-12)\
> An invalid customer reference returns an empty list, so the agent cannot tell a bad reference from a valid search with no matches. Return a structured validation error with a stable code and a safe next step.

Each finding names the affected tool, points to compact evidence, explains the impact, and suggests a concrete fix. The report also lists checks that were skipped, so an incomplete review is not mistaken for a pass.

## How it works

1. **You identify a non-production server.** Provide a `dev`, `test`, or `staging` environment and, if you have them, the tasks you want reviewed.
2. **The skill inspects the agent-facing contract.** It reviews tool names, descriptions, schemas, annotations, overlaps, and result boundaries against mcp-sauna’s written rules.
3. **It runs bounded, safe probes.** It uses your confirmed tasks, respects call and response limits, and never calls destructive tools. Write probes are off unless explicitly enabled and individually confirmed.
4. **You get a scorecard and prioritized fixes.** A bundled grader applies the same severity rules every time. The skill recommends changes; it does not edit your server.

The model judges findings from the definitions and observed evidence. The local grader handles the arithmetic. Checks that could not be run safely are marked **incomplete**, not counted as passes.

## What you get

The agent saves three files in its workspace:

- **`report.md`** — the human-readable scorecard, findings, evidence references, task outcomes, and skipped probes;
- **`results.json`** — the same review in machine-readable form, useful for comparing runs or building your own reporting;
- **`run.json`** — a sanitized input record containing tool and field names, counts, outcomes, and estimates, not raw arguments or result values.

The scorecard covers five areas: **Tool design, Context cost, Responses, Errors, and Safety.** Findings have stable rule IDs and severity levels, so you can see what matters most and compare future runs. If a check cannot safely run, the overall result stays **incomplete** until the relevant coverage is available.

See the [sample report](examples/report.example.md) for the full format. The stable checks are published as the versioned [mcp-sauna rules v1 standard](standards/mcp-sauna-rules-v1.md).

## Try it

1. Install the repository’s root skill folder in your agent’s skills directory:
   - Claude Code: `.claude/skills/mcp-sauna/`
   - Codex: `.agents/skills/mcp-sauna/`
   - GitHub Copilot: `.github/skills/mcp-sauna/`
2. Connect your MCP server to the agent as usual, using a non-production environment.
3. Ask: **“Put the `erp-dev` MCP server through mcp-sauna.”**

If you provide a task file, mcp-sauna uses those tasks. Otherwise, it drafts realistic tasks from the tool list and asks you to confirm them before behavioral probes. It then saves the report files in the agent’s workspace.

For a manual install, copy `SKILL.md`, `references/`, `standards/`, `scripts/`, and `examples/` into the host’s `mcp-sauna` skills folder. Keep them together so the skill can load its rules, report format, and grader. The agent runs the bundled grader automatically when Python 3.10+ is available; otherwise it applies the same grading formula itself. There is no hosted mcp-sauna service.

## Safety and limits

- Production is out of scope. The skill stops if the environment is production or appears production-like.
- Read probes are the default. Every enabled write call needs separate confirmation; destructive tools are never called.
- Reviews are bounded by time, call count, and response size. The skill stops when a result is unexpectedly large or sensitive.
- Reports omit raw arguments and result values. Tool output still passes through the model provider already used by your agent.
- mcp-sauna is a design review, not a security audit, penetration test, or MCP protocol conformance suite.

## Release status

**mcp-sauna v1.0.0 is a stable release.** The rules standard is versioned independently as [mcp-sauna rules v1](standards/mcp-sauna-rules-v1.md). Recorded host validation is from v0.1: Codex and Claude Code passed the reference checks, while GitHub Copilot was not tested. v1.0.0 has not had a fresh cross-host evaluation, so exact host parity is unverified. See the [historical evaluation matrix](eval/agent-matrix-v0.1.json), [sanitized reports](eval/artifacts/), and the [project site](https://prspktvs.github.io/mcp-sauna/).

For project development, reference-server evaluation, and release validation, see [CONTRIBUTING.md](CONTRIBUTING.md). Maintainer scripts and multi-agent checks are documented there.

## License

Apache-2.0. See [LICENSE](LICENSE).
