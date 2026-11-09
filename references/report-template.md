# Run log and report format

The skill should create a sanitized `run.json` input for `scripts/grade.py`. The grader emits `results.json` and `report.md` with the same findings, scorecard, and metrics. Do not include raw call arguments, result values, credentials, full tool responses, personal data, or unmasked examples.

## Sanitized run.json input

Use this shape (all top-level fields required unless noted):

```json
{
  "schema_version": 1,
  "run": {
    "environment": "test",
    "agent": "Codex",
    "model": "model name or unknown",
    "date": "2026-11-09",
    "skill_version": "0.1.0",
    "target_label": "local test server"
  },
  "tool_definitions": [
    {
      "name": "search_orders",
      "description": "Find orders by name or status; use this instead of listing every order.",
      "input_schema": {"type": "object", "properties": {}, "required": []},
      "output_schema": null,
      "annotations": {"readOnlyHint": true, "destructiveHint": false}
    }
  ],
  "tasks": [
    {"id": "TASK-01", "success": true, "attempts": 1, "tool_calls": 2, "estimated_tokens": 340}
  ],
  "calls": [
    {
      "id": "CALL-01",
      "phase": "P1",
      "task_id": "TASK-01",
      "identity": null,
      "tool": "search_orders",
      "argument_fields": ["query", "limit"],
      "result_fields": ["orders", "next_cursor"],
      "result_items": 3,
      "result_bytes": 800,
      "estimated_tokens": 200,
      "outcome": "success",
      "error_class": null
    }
  ],
  "findings": [
    {
      "id": "F-01",
      "rule_id": "R1",
      "severity": "High",
      "tool": "list_orders",
      "evidence_call_ids": ["CALL-04"],
      "summary": "The list response has no continuation or total indicator.",
      "why_it_matters": "The caller cannot tell whether the result is complete.",
      "fix": "Add a bounded limit and a cursor or explicit has_more/total field."
    }
  ],
  "skipped_probes": [
    {"probe_id": "P4", "reason": "Only one test identity was configured."}
  ]
}
```

Allowed call `outcome` values: `success`, `error`, `skipped`. `phase` is `static` or `P1`–`P6`. Tool definitions are needed only for C1/static evidence; they are not copied to the final report. Each call entry stores field names and sizes/counts, never argument or result values. Use `error_class` such as `validation`, `not_found`, `permission`, or `transport`; do not store raw error text.

`identity` is `A` or `B` only for a P4 call through the corresponding configured test connection; otherwise it is null. `estimated_tokens` uses provider usage if exposed. Otherwise estimate from UTF-8 bytes divided by four, round up, and label aggregate metrics as estimates. Avoid false precision.

## Report layout

The generated Markdown report contains:

1. Summary: overall grade, one-line verdict, and up to three prioritized fixes.
2. Scorecard: grades for Tool design (T), Context cost (C), Responses (R), Errors (E), and Safety (S), plus complete/incomplete status.
3. Metrics: task success rate, average tool calls and estimated tokens per task, estimated tool-definition tokens, unsafe behaviors found, and total calls.
4. Findings by severity: rule ID, tool, call references, issue, impact, and fix.
5. Not tested: skipped probes and reason.
6. Run details: environment, agent, model, date, call count, and skill version.
7. Footer: “This is an automated design review, not a security audit.” Also state that tool output passed through the model provider already used by the agent. Link “Book a full design review” to the URL configured by the publisher as `MCP_SAUNA_BOOKING_URL`; if it is unset, make the missing publisher configuration explicit and do not invent a URL.

## Grade calculation

For each dimension, use the worst finding mapped to its rules: none=A, Low=B, Medium=C, High=D, Critical=F. The overall grade is the worst of the five dimension grades only when all five dimensions are complete. If any dimension has a skipped or inconclusive probe required by its rules and no finding already establishes its grade, mark that dimension `incomplete` and the overall grade `incomplete`; do not count skipped checks as A. A dimension can show both a known grade and `incomplete` status when some of its rules were assessed and another relevant probe was skipped. See the rule-to-dimension mapping in `scripts/grade.py`.
