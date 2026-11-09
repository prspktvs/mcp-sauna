# mcp-sauna review report

**Overall grade: incomplete** — The review is incomplete; skipped probes are not counted as passes.

## Summary

Top fixes:

- **S1 (place_order):** Publish accurate annotations (place_order: readOnlyHint false, destructiveHint per behavior, idempotentHint true with its key) and confirm the host forwards them.

## Scorecard

| Dimension | Grade | Status | Findings |
| --- | --- | --- | ---: |
| Tool design | A | complete | 0 |
| Context cost | A | complete | 0 |
| Responses | A | complete | 0 |
| Errors | A | incomplete | 0 |
| Safety | C | incomplete | 1 |
| | | Incomplete: P2 skipped: Empty required-ID input not tested: host schema enforces minLength on required inputs and validation was not bypassed. Only the malformed-date case ran. | |
| | | Incomplete: P5 skipped: Write probes disabled by the user. | |

## Metrics

- Task success rate: 2/6 attempted (33%); 2 skipped
- Average tool calls per task: 1.7
- Average estimated tokens per task: 74 (estimate)
- Tool definitions: 1314 estimated tokens (5254 UTF-8 bytes)
- Unsafe behaviors found: 1
- Total tool calls: 14

## Findings

### Medium: S1 — place_order

No mutation annotations (readOnlyHint/destructiveHint/idempotentHint) are visible to the agent for the state-changing place_order tool; whether the gap is in the server or the host is unknown.

**Why it matters:** Without agent-visible annotations, clients cannot reliably distinguish the write tool from read tools or apply approval policy.

**Fix:** Publish accurate annotations (place_order: readOnlyHint false, destructiveHint per behavior, idempotentHint true with its key) and confirm the host forwards them.

## Not tested

- P2 skipped: Empty required-ID input not tested: host schema enforces minLength on required inputs and validation was not bypassed. Only the malformed-date case ran.
- P5 skipped: Write probes disabled by the user.

## Run details

- Environment: test
- Target: good_a / good_b local synthetic test servers
- Agent/model: Claude Code / claude-sonnet-5-5
- Date: 2026-11-09
- Calls: 14
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent.

This is an automated design review, not a security audit.

Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.
