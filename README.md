# mcp-sauna

An Agent Skill that reviews MCP server tool design and behavior, then produces a prioritized scorecard. It does not edit your server.

## Use it

1. Install this repository's root skill folder in your agent's skills directory:
   - Claude Code: `.claude/skills/mcp-sauna/`
   - Codex: `.agents/skills/mcp-sauna/`
   - GitHub Copilot: `.github/skills/mcp-sauna/`
2. Connect your MCP server to the agent as usual, using a `dev`, `test`, or `staging` environment.
3. Ask: “Put the `erp-test` MCP server through mcp-sauna.”

The agent guides the review and creates `report.md` and `results.json`. **You do not need to run Python, install project dependencies, start the reference servers, or use multiple agents.** The agent performs scoring automatically; it uses the bundled local grader when Python 3.10+ is available and otherwise applies the same grade formula itself.

The review is read-only by default, never calls destructive tools, and is a design review rather than a security audit. It asks you to confirm drafted tasks before probing and requires separate confirmation for every enabled write call.

## Prerelease status

Codex passed the reference checks twice with stable high-severity findings. Claude Code and GitHub Copilot have not yet been validated. See the [release matrix](eval/agent-matrix-v0.1.json). This release is a prerelease until cross-agent validation is complete.

## Contributing

Reference-server setup, Python scripts, automated tests, and cross-agent release checks are maintainer workflows. They are documented in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0. See [LICENSE](LICENSE).
