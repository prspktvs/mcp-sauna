# mcp-sauna example report: naive reference server

> Fictional test data only. This example shows the report shape; run the skill for current findings.

## Summary

**Overall grade: incomplete** (the known worst dimension grade is F) — the reference server exposes broad endpoint-shaped tools, weak result boundaries, and unsafe write design. The most urgent fixes are to split mixed read/write operations, add pagination and actionable errors, and separate permissions by identity.

## Scorecard

| Dimension | Grade | Status |
| --- | --- | --- |
| Tool design (T) | D | Complete |
| Context cost (C) | C | Complete |
| Responses (R) | D | Complete |
| Errors (E) | D | Complete |
| Safety (S) | F | Incomplete |

## Metrics

- Task success: 1/3 (33%)
- Average tool calls per task: 2.3
- Average tool tokens per task: approximately 1,120 (estimate)
- Tool-definition tokens: approximately 5,600 (estimate)
- Unsafe behaviors found: 2

## Findings

### Critical

- **S5 — Shared identity permissions** (`list_invoices`, CALL-12): Both configured test identities received the same restricted invoice record. Split authorization by caller identity and verify the policy at the server boundary.

### High

- **R1 — Unbounded list/search** (`list_orders`, CALL-08): The broad list returned no continuation metadata. Add a maximum page size, cursor, and total/has-more indicator.
- **E1 — Unhelpful error response** (`get_order`, CALL-09): An invalid identifier produced an unclassified server error. Return a stable error code and a safe next step.
- **S3 — Risky write without a preview/confirmation boundary** (`create_order`): Static review found no preview token or confirmation flow. Add a review step before committing the order.

## Not tested

- P5 skipped: the user did not enable write probes. Safety is marked incomplete even though the observed S5 finding already gives it an F.

## Run details

- Environment: test
- Agent/model: example only
- Date: 2026-11-09
- Calls: 14
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent. This is an automated design review, not a security audit.
