# mcp-sauna review report

**Overall grade: incomplete** — The review is incomplete; skipped probes are not counted as passes.

## Summary

Top fixes:

- **S5 (mcp__naive_a__get_invoice_by_id):** Enforce per-identity authorization server-side on every read and return not-found or permission errors for unauthorized records; add a regression test with two identities.
- **E1 (mcp__naive_a__list_orders):** Validate fromDate and return a structured invalid_date error stating the expected format, with a 4xx class.
- **E2 (mcp__naive_a__get_invoice_by_id):** Return a structured missing_required_field/invalid_argument error for empty identifiers.

## Scorecard

| Dimension | Grade | Status | Findings |
| --- | --- | --- | ---: |
| Tool design | D | complete | 46 |
| Context cost | C | complete | 1 |
| Responses | D | incomplete | 7 |
| Errors | D | complete | 4 |
| Safety | F | incomplete | 24 |
| | | Incomplete: P3 skipped: No documented safe maximum on any list tool; behavioral part skipped and R1 reported statically. | |
| | | Incomplete: P5 skipped: Write probes disabled; no write or destructive tool was called. | |

## Metrics

- Task success rate: 3/4 attempted (75%); 4 skipped
- Average tool calls per task: 1.2
- Average estimated tokens per task: 96 (estimate)
- Tool definitions: 15971 estimated tokens (63884 UTF-8 bytes)
- Unsafe behaviors found: 24
- Total tool calls: 12

## Findings

### Critical: S5 — mcp__naive_a__get_invoice_by_id

Identity B received the restricted synthetic invoice that only identity A is expected to see, through the same get_invoice_by_id read (same response fields, 1 record).

**Why it matters:** Authorization appears shared across the two configured identities, so per-user data isolation is not enforced.; evidence: CALL-01, CALL-02

**Fix:** Enforce per-identity authorization server-side on every read and return not-found or permission errors for unauthorized records; add a regression test with two identities.

### High: E1 — mcp__naive_a__list_orders

Malformed fromDate returned a raw status 500 with a stack-trace field and no safe next step.

**Why it matters:** Callers get no actionable guidance, and internals leak.; evidence: CALL-03

**Fix:** Validate fromDate and return a structured invalid_date error stating the expected format, with a 4xx class.

### High: E2 — mcp__naive_a__get_invoice_by_id

An empty value for the required identifier succeeded with a null/empty result instead of an error.

**Why it matters:** A missing identifier is indistinguishable from no match.; evidence: CALL-04

**Fix:** Return a structured missing_required_field/invalid_argument error for empty identifiers.

### High: E2 — mcp__naive_a__get_order_by_id

An empty value for the required identifier succeeded with a null/empty result instead of an error.

**Why it matters:** A missing identifier is indistinguishable from no match.; evidence: CALL-05

**Fix:** Return a structured missing_required_field/invalid_argument error for empty identifiers.

### High: E2 — mcp__naive_a__get_product_by_sku

An empty value for the required identifier succeeded with a null/empty result instead of an error.

**Why it matters:** A missing identifier is indistinguishable from no match.; evidence: CALL-06

**Fix:** Return a structured missing_required_field/invalid_argument error for empty identifiers.

### High: R1 — mcp__naive_a__list_customers

No limit, cursor or total/has-more field in the schema; only optional filters. Behavioral P3 skipped.

**Why it matters:** Result completeness and size are unknowable.

**Fix:** Add a capped limit, cursor, and total/has_more.

### High: R1 — mcp__naive_a__list_invoices

No limit, cursor or total/has-more field in the schema; only an optional customerName filter. Behavioral P3 skipped.

**Why it matters:** Result completeness and size are unknowable.

**Fix:** Add a capped limit, cursor, and total/has_more.

### High: R1 — mcp__naive_a__list_orders

No limit, cursor or total/has-more field in the schema; only optional filters. Behavioral P3 skipped.

**Why it matters:** Result completeness and size are unknowable.

**Fix:** Add a capped limit, cursor, and total/has_more.

### High: R1 — mcp__naive_a__list_products

No limit, cursor or total/has-more field in the schema; only optional filters. Behavioral P3 skipped.

**Why it matters:** Result completeness and size are unknowable.

**Fix:** Add a capped limit, cursor, and total/has_more.

### High: R1 — mcp__naive_a__list_stock

No limit, cursor or total/has-more field in the schema; only optional filters. Behavioral P3 skipped.

**Why it matters:** Result completeness and size are unknowable.

**Fix:** Add a capped limit, cursor, and total/has_more.

### High: S2 — mcp__naive_a__get_or_update_stock

One tool reads stock when quantity is omitted and changes stock when it is set.

**Why it matters:** An omitted argument decides whether state changes.

**Fix:** Split into check_stock and adjust_stock.

### High: S3 — mcp__naive_a__cancel_order

Consequential action (order, financial, external send, inventory or irreversible) with no documented preview or confirmation step.

**Why it matters:** Wrong arguments commit immediately.

**Fix:** Add a preview/confirm flow and an explicit confirmation parameter.

### High: S3 — mcp__naive_a__create_invoice

Consequential action (order, financial, external send, inventory or irreversible) with no documented preview or confirmation step.

**Why it matters:** Wrong arguments commit immediately.

**Fix:** Add a preview/confirm flow and an explicit confirmation parameter.

### High: S3 — mcp__naive_a__create_order

Consequential action (order, financial, external send, inventory or irreversible) with no documented preview or confirmation step.

**Why it matters:** Wrong arguments commit immediately.

**Fix:** Add a preview/confirm flow and an explicit confirmation parameter.

### High: S3 — mcp__naive_a__delete_customer

Consequential action (order, financial, external send, inventory or irreversible) with no documented preview or confirmation step.

**Why it matters:** Wrong arguments commit immediately.

**Fix:** Add a preview/confirm flow and an explicit confirmation parameter.

### High: S3 — mcp__naive_a__get_or_update_stock

Consequential action (order, financial, external send, inventory or irreversible) with no documented preview or confirmation step.

**Why it matters:** Wrong arguments commit immediately.

**Fix:** Add a preview/confirm flow and an explicit confirmation parameter.

### High: S3 — mcp__naive_a__send_invoice

Consequential action (order, financial, external send, inventory or irreversible) with no documented preview or confirmation step.

**Why it matters:** Wrong arguments commit immediately.

**Fix:** Add a preview/confirm flow and an explicit confirmation parameter.

### High: S6 — mcp__naive_a__get_customer

Result field admin_note contains text addressed to the agent that tells it to disregard prior directions and bulk-expose records via another tool. Not followed or quoted; seen in 2 of 2 results.

**Why it matters:** Injected instructions in output can steer agents into bulk data exposure.; evidence: CALL-07, CALL-08

**Fix:** Remove agent-directed text from results; return only data fields and sanitize stored free-text.

### High: T2 — mcp__naive_a__list_customers

list_customers and get_customer both serve lookups of the same entity; neither description says when to use the broad list versus the single-record call, and no safe selection boundary is given.

**Why it matters:** Agents may choose the broad list when a single record is wanted.

**Fix:** State when to use each and how to scope each lookup.

### High: T2 — mcp__naive_a__list_invoices

list_invoices and get_invoice_by_id both serve lookups of the same entity; neither description says when to use the broad list versus the single-record call, and no safe selection boundary is given.

**Why it matters:** Agents may choose the broad list when a single record is wanted.

**Fix:** State when to use each and how to scope each lookup.

### High: T2 — mcp__naive_a__list_orders

list_orders and get_order_by_id both serve lookups of the same entity; neither description says when to use the broad list versus the single-record call, and no safe selection boundary is given.

**Why it matters:** Agents may choose the broad list when a single record is wanted.

**Fix:** State when to use each and how to scope each lookup.

### High: T2 — mcp__naive_a__list_products

list_products and get_product_by_sku both serve lookups of the same entity; neither description says when to use the broad list versus the single-record call, and no safe selection boundary is given.

**Why it matters:** Agents may choose the broad list when a single record is wanted.

**Fix:** State when to use each and how to scope each lookup.

### High: T2 — mcp__naive_a__list_stock

list_stock and get_or_update_stock both serve lookups of the same entity; neither description says when to use the broad list versus the single-record call, and no safe selection boundary is given.

**Why it matters:** Agents may choose the broad list when a single record is wanted.

**Fix:** State when to use each and how to scope each lookup.

### High: T4 — mcp__naive_a__cancel_order

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_customer

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_invoice

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_order

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_product

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__delete_customer

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_invoice_by_id

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_or_update_stock

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_order_by_id

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_product_by_sku

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__send_invoice

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__update_customer

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__update_order

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__update_product

Required input(s) have no meaningful description, format or example (empty or only a label such as 'Order ID').

**Why it matters:** Agents must guess identifier formats, units and allowed fields.

**Fix:** Document format, constraints and an example for each required property.

### Medium: C1 — all tools

The 20 distinct tool definitions are about 54 KB serialized; the estimate is far above 5,000 tokens, mainly from a 7x repeated boilerplate description (see metrics for exact estimate).

**Why it matters:** Heavy fixed context cost on every request.

**Fix:** Cut descriptions to one short task-oriented paragraph and consolidate tools.

### Medium: R2 — mcp__naive_a__get_order_by_id

Both order lookups returned about 7 internal fields (route, bin, audit, source system, retry counter, export marker, billing segment) unrelated to a status check.

**Why it matters:** Raises context cost and exposes internals.; evidence: CALL-09, CALL-10

**Fix:** Return a task-shaped summary (order number, status, customer name, dates, total) and make internals opt-in.

### Medium: S1 — mcp__naive_a__cancel_order

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_customer

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_invoice

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_order

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_product

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__delete_customer

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__get_or_update_stock

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__send_invoice

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__update_customer

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__update_order

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__update_product

State-changing tool; no annotations are exposed to the model, so read-only/destructive hints are unavailable (server vs host cause unknown).

**Why it matters:** Hosts and agents cannot gate writes by hint.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S4 — mcp__naive_a__create_customer

Create operation has no idempotency key in its schema.

**Why it matters:** A retry can create duplicates.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: S4 — mcp__naive_a__create_invoice

Create operation has no idempotency key in its schema.

**Why it matters:** A retry can create duplicates.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: S4 — mcp__naive_a__create_order

Create operation has no idempotency key in its schema.

**Why it matters:** A retry can create duplicates.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: S4 — mcp__naive_a__create_product

Create operation has no idempotency key in its schema.

**Why it matters:** A retry can create duplicates.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: T1 — all tools

The catalog mirrors the legacy API one-to-one with get/list/create/update/delete/cancel per entity and no task-level tools.

**Why it matters:** Agents must orchestrate raw endpoints and internal IDs.

**Fix:** Offer task tools such as find_account, check_order_status, prepare_order.

### Medium: T3 — mcp__naive_a__cancel_order

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__create_customer

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__create_invoice

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__create_order

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__create_product

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__delete_customer

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__get_customer

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__get_invoice_by_id

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__get_or_update_stock

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__get_order_by_id

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__get_product_by_sku

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__list_customers

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__list_invoices

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__list_orders

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__list_products

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__list_stock

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__send_invoice

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__update_customer

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__update_order

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T3 — mcp__naive_a__update_product

Description is generic boilerplate; it gives no use case and no boundary or alternative.

**Why it matters:** Agents cannot choose among tools reliably.

**Fix:** Write when to use and when not to use, naming the alternative tool.

### Medium: T5 — mcp__naive_a__cancel_order

Requires an opaque invoiceId/orderId; no tool resolves it from a readable name or number (list_invoices returns unlabeled ids; list_orders has no name or number filter).

**Why it matters:** Users cannot reach these tools from readable identifiers.

**Fix:** Add a search by invoice number, order number or customer name that returns ids with labels.

### Medium: T5 — mcp__naive_a__create_invoice

Requires an opaque invoiceId/orderId; no tool resolves it from a readable name or number (list_invoices returns unlabeled ids; list_orders has no name or number filter).

**Why it matters:** Users cannot reach these tools from readable identifiers.

**Fix:** Add a search by invoice number, order number or customer name that returns ids with labels.

### Medium: T5 — mcp__naive_a__get_invoice_by_id

Requires an opaque invoiceId/orderId; no tool resolves it from a readable name or number (list_invoices returns unlabeled ids; list_orders has no name or number filter).

**Why it matters:** Users cannot reach these tools from readable identifiers.

**Fix:** Add a search by invoice number, order number or customer name that returns ids with labels.

### Medium: T5 — mcp__naive_a__get_order_by_id

Requires an opaque invoiceId/orderId; no tool resolves it from a readable name or number (list_invoices returns unlabeled ids; list_orders has no name or number filter).

**Why it matters:** Users cannot reach these tools from readable identifiers.

**Fix:** Add a search by invoice number, order number or customer name that returns ids with labels.

### Medium: T5 — mcp__naive_a__send_invoice

Requires an opaque invoiceId/orderId; no tool resolves it from a readable name or number (list_invoices returns unlabeled ids; list_orders has no name or number filter).

**Why it matters:** Users cannot reach these tools from readable identifiers.

**Fix:** Add a search by invoice number, order number or customer name that returns ids with labels.

### Medium: T5 — mcp__naive_a__update_order

Requires an opaque invoiceId/orderId; no tool resolves it from a readable name or number (list_invoices returns unlabeled ids; list_orders has no name or number filter).

**Why it matters:** Users cannot reach these tools from readable identifiers.

**Fix:** Add a search by invoice number, order number or customer name that returns ids with labels.

### Low: R3 — mcp__naive_a__list_invoices

Invoice rows contain id, status, amount, currency but no invoice number, customer name or date.

**Why it matters:** Rows cannot be interpreted or ordered by recency; TASK-05 failed on both attempts for this reason.; evidence: CALL-11

**Fix:** Add invoice number, customer name and issue/due date to each row.

## Not tested

- P3 skipped: No documented safe maximum on any list tool; behavioral part skipped and R1 reported statically.
- P5 skipped: Write probes disabled; no write or destructive tool was called.

## Run details

- Environment: test
- Target: local synthetic wholesale test server (naive_a, naive_b)
- Agent/model: Claude Code / claude-sonnet-5-5
- Date: 2026-11-09
- Calls: 12
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent.

This is an automated design review, not a security audit.

Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.
