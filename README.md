# mcp-sauna

**Find out whether your MCP server gives an AI agent the right tools for the job.**

mcp-sauna is an open-source Agent Skill for developers building or inheriting MCP servers. It reviews the server's tools the way a model encounters them, then gives you a scorecard and a prioritized list of design fixes.

## Why use it?

An MCP server can work correctly at the protocol level and still be difficult for an agent to use. Tool names may mirror backend endpoints instead of user tasks. Descriptions may not tell the model which tool to choose. Required inputs may be vague, searches may return too much, and errors may give no useful next step. State-changing tools can also be hard to distinguish from reads.

Those are interface problems. Rewriting prompts around them can hide a symptom without improving the tool contract. mcp-sauna helps you find and describe the contract issues so you can fix them at the server boundary.

## How the review works

The skill follows five steps:

1. Confirms the target and a `dev`, `test`, or `staging` environment.
2. Reviews tool names, descriptions, schemas, annotations, and overlaps against written design rules.
3. Plans bounded probes using tasks you provide or approve.
4. Runs safe reads to check task completion, errors, result size, and permissions when two test identities are available.
5. Produces a report with evidence and concrete fixes.

The model decides whether a rule applies based on the tool contract and observed evidence. A bundled local grader applies fixed severities and calculates the scorecard, so arithmetic is consistent. Skipped probes are marked incomplete; they do not count as passes.

## What you get

The review creates:

- **`report.md`** — an overview, scorecard, prioritized findings, evidence references, and skipped checks.
- **`results.json`** — the same findings in machine-readable form for comparing reviews over time.
- **`run.json`** — a sanitized record used to produce the report. It contains tool and field names, counts, and outcome metadata, not raw arguments or result values.

The scorecard covers five areas: **Tool design, Context cost, Responses, Errors, and Safety.** Findings use stable rule IDs and four severity levels:

| Finding severity | Dimension grade |
| --- | --- |
| No finding established | A |
| Low | B |
| Medium | C |
| High | D |
| Critical | F |

The overall grade is the worst dimension grade when the review is complete. If a required check could not be run safely, the affected dimension and overall result are marked **incomplete**. A finding includes the affected tool, evidence reference, why it matters, and a suggested fix.

**Example finding:** A search tool has no maximum page size or continuation signal. mcp-sauna reports the applicable rule, the tool and evidence, explains that results may be incomplete or too large, and recommends a bounded limit with pagination metadata.

See the [sample report](examples/report.example.md) for the full report layout.

## Use it

1. Install the repository's root skill folder in your agent's skills directory:
   - Claude Code: `.claude/skills/mcp-sauna/`
   - Codex: `.agents/skills/mcp-sauna/`
   - GitHub Copilot: `.github/skills/mcp-sauna/`
2. Connect your MCP server to the agent as usual, using a non-production environment.
3. Ask: **“Put the `erp-dev` MCP server through mcp-sauna.”**

If you provide a task file, the skill uses those tasks. Otherwise, it drafts tasks from the tool list and asks you to confirm them before probing. It then saves the report artifacts in the agent's workspace.

To install manually, clone this repository and copy `SKILL.md`, `references/`, `scripts/`, and `examples/` into the host's `mcp-sauna` skills folder. Keep those files together so the skill can load its rules, report format, and grader.

**You do not need to run Python or project scripts, start the reference servers, or use multiple agents.** The agent runs the bundled grader automatically when Python 3.10+ is available; otherwise it applies the same grading formula itself. There is no hosted mcp-sauna service.

## Safety and limits

- Production is out of scope. The skill stops if the environment is production or appears production-like.
- Probes are read-only by default. Every enabled write call needs separate confirmation; destructive tools are never called.
- Calls and review time are bounded. The skill stops on unexpectedly large or sensitive results.
- Reports omit raw call arguments and result values. Tool output still passes through the model provider already used by your agent.
- mcp-sauna is a design review, not a security audit, penetration test, or MCP protocol conformance suite. It recommends changes but never edits your server.

## Release status

This is a prerelease. Codex passed the naive reference checks twice with stable high-severity findings and had no High or Critical findings on the good reference. Claude Code and GitHub Copilot have not yet been validated. See the [evaluation matrix](eval/agent-matrix-v0.1.json) and [sanitized reports](eval/artifacts/).

For project development, reference-server evaluation, and release validation, see [CONTRIBUTING.md](CONTRIBUTING.md). Maintainer scripts and multi-agent checks are documented there.

## License

Apache-2.0. See [LICENSE](LICENSE).
