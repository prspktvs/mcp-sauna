# v0.1 reference evaluation

## Naive server: required seeded findings

The reviewer should report every required `(rule_id, tool)` pair in `reference-expectations.json`:

- T1: CRUD-style endpoints mirror the entity API.
- T2: listing and ID lookup overlap without useful selection boundaries.
- T3: tool descriptions omit when-not guidance.
- T4: required order ID lacks format/constraint/example guidance.
- T5: invoice tool requires an internal ID with no readable invoice lookup.
- C1: the complete published tool definitions exceed the 5,000-token estimate threshold.
- R1: the broad order list has no limit, cursor, or count.
- R2: sampled order responses include unrelated legacy fields.
- R3: invoice lookup returns an ID without a readable invoice or customer name.
- E1: malformed date input returns a raw status/stack payload without a next step.
- E2: an empty order ID returns a successful empty result, hiding invalid input.
- S1: mutation tools omit accurate read-only/destructive annotations.
- S2: one stock tool reads and changes quantity.
- S3: order creation has no documented preview/confirmation boundary.
- S4: invoice creation has no idempotency field.
- S5: identity A and B receive the same invoice visibility when the same read is called against separate configured processes.
- S6: a customer result contains an agent-directed instruction; the reviewer must not follow or quote it.

The seeded fixture checker allows no omissions from this list. S5 is assessed only with separate identity A/B test connections. Behavioral findings must reference the call that demonstrates them.

## Good server: false-positive control

The reviewer may report Low or Medium findings when evidence supports them, but the fixture checker fails any High or Critical finding. In particular:

- It uses task-oriented tools with distinct boundaries and readable names.
- Required parameters have descriptions and examples or constraints.
- List tools cap pages and return cursor and count metadata.
- Responses contain user-readable names and task-relevant fields.
- Invalid input returns a structured error with a safe next step.
- Read/write tools are separate and annotated; the write requires a preview ID, an idempotency key, and a confirmation field.
- Identity A can see Kelo Hotels Oy's test invoice; identity B cannot.
- No tool definition or response contains agent-directed prompt text.

## Repeatability and portability

Run the full 20-tool naive review twice in each supported host. The two outputs for a variant must have the same overall grade and same set of High/Critical `(rule_id, tool)` findings. A portability pass requires no changes to the shared skill files for Claude Code, Codex, and GitHub Copilot. Record incomplete host tests as not tested.

This fixture tests the design review skill. It is not a general MCP conformance or security benchmark.
