# mcp-sauna review report

**Overall grade: incomplete** — The review is incomplete; skipped probes are not counted as passes.

## Summary

Top fixes:

- **S5 (mcp__naive_a__get_invoice_by_id):** Enforce per-identity authorization server-side on every read and return a permission error or no record for unauthorized callers; add a regression test with two identities.
- **E1 (mcp__naive_a__list_orders):** Validate fromDate and return a structured 4xx error such as invalid_date with the expected YYYY-MM-DD format.
- **E2 (mcp__naive_a__get_invoice_by_id):** Reject empty identifiers (minLength 1) and return a structured missing_required_field error.

## Scorecard

| Dimension | Grade | Status | Findings |
| --- | --- | --- | ---: |
| Tool design | D | complete | 46 |
| Context cost | C | complete | 1 |
| Responses | D | incomplete | 7 |
| Errors | D | complete | 4 |
| Safety | F | incomplete | 24 |
| | | Incomplete: P3 skipped: No documented safe maximum page size on any list tool; unbounded request not allowed. R1 reported statically. | |
| | | Incomplete: P5 skipped: Write probes disabled; no write or destructive tool was called. | |

## Metrics

- Task success rate: 3/4 attempted (75%); 4 skipped
- Average tool calls per task: 1.2
- Average estimated tokens per task: 82 (estimate)
- Tool definitions: 15946 estimated tokens (63782 UTF-8 bytes)
- Unsafe behaviors found: 24
- Total tool calls: 11

## Findings

### Critical: S5 — mcp__naive_a__get_invoice_by_id

Identity B received the same restricted synthetic invoice record (INV-ID-501) as identity A for the identical read; B was expected to be denied. Observed in P4.

**Why it matters:** Authorization appears shared across identities, so restricted records leak between principals.; evidence: CALL-05, CALL-06

**Fix:** Enforce per-identity authorization server-side on every read and return a permission error or no record for unauthorized callers; add a regression test with two identities.

### High: E1 — mcp__naive_a__list_orders

The malformed fromDate returned a raw status 500 with a stack-trace-style field and no safe next step (error class: server_error).

**Why it matters:** The agent cannot self-correct and internal code paths are exposed.; evidence: CALL-01

**Fix:** Validate fromDate and return a structured 4xx error such as invalid_date with the expected YYYY-MM-DD format.

### High: E2 — mcp__naive_a__get_invoice_by_id

An empty required identifier succeeded with an empty/null result instead of a validation error.

**Why it matters:** A missing identifier is indistinguishable from a record that does not exist.; evidence: CALL-03

**Fix:** Reject empty identifiers (minLength 1) and return a structured missing_required_field error.

### High: E2 — mcp__naive_a__get_order_by_id

An empty required identifier succeeded with an empty/null result instead of a validation error.

**Why it matters:** A missing identifier is indistinguishable from a record that does not exist.; evidence: CALL-02

**Fix:** Reject empty identifiers (minLength 1) and return a structured missing_required_field error.

### High: E2 — mcp__naive_a__get_product_by_sku

An empty required identifier succeeded with an empty/null result instead of a validation error.

**Why it matters:** A missing identifier is indistinguishable from a record that does not exist.; evidence: CALL-04

**Fix:** Reject empty identifiers (minLength 1) and return a structured missing_required_field error.

### High: R1 — mcp__naive_a__list_customers

No limit, cursor or total/has-more field in the input schema; the behavioral P3 probe was skipped because no safe maximum is documented.

**Why it matters:** Result size is unbounded and completeness cannot be judged.

**Fix:** Add a capped limit, a cursor and count/has_more fields to the response.

### High: R1 — mcp__naive_a__list_invoices

No limit, cursor or total/has-more field in the input schema; the behavioral P3 probe was skipped because no safe maximum is documented.

**Why it matters:** Result size is unbounded and completeness cannot be judged.

**Fix:** Add a capped limit, a cursor and count/has_more fields to the response.

### High: R1 — mcp__naive_a__list_orders

No limit, cursor or total/has-more field in the input schema; the behavioral P3 probe was skipped because no safe maximum is documented.

**Why it matters:** Result size is unbounded and completeness cannot be judged.

**Fix:** Add a capped limit, a cursor and count/has_more fields to the response.

### High: R1 — mcp__naive_a__list_products

No limit, cursor or total/has-more field in the input schema; the behavioral P3 probe was skipped because no safe maximum is documented.

**Why it matters:** Result size is unbounded and completeness cannot be judged.

**Fix:** Add a capped limit, a cursor and count/has_more fields to the response.

### High: R1 — mcp__naive_a__list_stock

No limit, cursor or total/has-more field in the input schema; the behavioral P3 probe was skipped because no safe maximum is documented.

**Why it matters:** Result size is unbounded and completeness cannot be judged.

**Fix:** Add a capped limit, a cursor and count/has_more fields to the response.

### High: S2 — mcp__naive_a__get_or_update_stock

The tool reads stock when quantity is omitted and changes stock when quantity is set (stated in its description).

**Why it matters:** Reads and consequential writes share one call, so an incomplete argument set can change inventory.

**Fix:** Split into check_stock (read-only) and adjust_stock (write with confirmation).

### High: S3 — mcp__naive_a__cancel_order

Consequential action (order, cancellation, deletion, external send, financial record, or stock change) has no documented preview, confirmation or equivalent safeguard.

**Why it matters:** The model can commit or send irreversibly in one call.

**Fix:** Add a preview/draft step and require an explicit confirmation token before commit.

### High: S3 — mcp__naive_a__create_invoice

Consequential action (order, cancellation, deletion, external send, financial record, or stock change) has no documented preview, confirmation or equivalent safeguard.

**Why it matters:** The model can commit or send irreversibly in one call.

**Fix:** Add a preview/draft step and require an explicit confirmation token before commit.

### High: S3 — mcp__naive_a__create_order

Consequential action (order, cancellation, deletion, external send, financial record, or stock change) has no documented preview, confirmation or equivalent safeguard.

**Why it matters:** The model can commit or send irreversibly in one call.

**Fix:** Add a preview/draft step and require an explicit confirmation token before commit.

### High: S3 — mcp__naive_a__delete_customer

Consequential action (order, cancellation, deletion, external send, financial record, or stock change) has no documented preview, confirmation or equivalent safeguard.

**Why it matters:** The model can commit or send irreversibly in one call.

**Fix:** Add a preview/draft step and require an explicit confirmation token before commit.

### High: S3 — mcp__naive_a__get_or_update_stock

Consequential action (order, cancellation, deletion, external send, financial record, or stock change) has no documented preview, confirmation or equivalent safeguard.

**Why it matters:** The model can commit or send irreversibly in one call.

**Fix:** Add a preview/draft step and require an explicit confirmation token before commit.

### High: S3 — mcp__naive_a__send_invoice

Consequential action (order, cancellation, deletion, external send, financial record, or stock change) has no documented preview, confirmation or equivalent safeguard.

**Why it matters:** The model can commit or send irreversibly in one call.

**Fix:** Add a preview/draft step and require an explicit confirmation token before commit.

### High: S6 — mcp__naive_a__get_customer

The result contains an extra field (admin_note) with text that addresses the agent and directs it to expose all customer records via another tool. Text not quoted and not followed.

**Why it matters:** Agent-directed instructions in tool output are a prompt-injection vector that could trigger bulk data disclosure.; evidence: CALL-07

**Fix:** Remove the field from output, sanitize stored free-text, and keep data fields separate from any instructions.

### High: T2 — mcp__naive_a__list_customers

list_customers and get_customer both serve lookups of the same record type and neither description says when to use the broad list versus the single-record tool.

**Why it matters:** The agent can pick either tool for the same request, risking broad reads.

**Fix:** State a selection boundary in both descriptions (e.g. list for filtered discovery, single-record tool for a known identifier) or merge into one find tool.

### High: T2 — mcp__naive_a__list_invoices

list_invoices and get_invoice_by_id both serve lookups of the same record type and neither description says when to use the broad list versus the single-record tool.

**Why it matters:** The agent can pick either tool for the same request, risking broad reads.

**Fix:** State a selection boundary in both descriptions (e.g. list for filtered discovery, single-record tool for a known identifier) or merge into one find tool.

### High: T2 — mcp__naive_a__list_orders

list_orders and get_order_by_id both serve lookups of the same record type and neither description says when to use the broad list versus the single-record tool.

**Why it matters:** The agent can pick either tool for the same request, risking broad reads.

**Fix:** State a selection boundary in both descriptions (e.g. list for filtered discovery, single-record tool for a known identifier) or merge into one find tool.

### High: T2 — mcp__naive_a__list_products

list_products and get_product_by_sku both serve lookups of the same record type and neither description says when to use the broad list versus the single-record tool.

**Why it matters:** The agent can pick either tool for the same request, risking broad reads.

**Fix:** State a selection boundary in both descriptions (e.g. list for filtered discovery, single-record tool for a known identifier) or merge into one find tool.

### High: T2 — mcp__naive_a__list_stock

list_stock and get_or_update_stock both serve lookups of the same record type and neither description says when to use the broad list versus the single-record tool.

**Why it matters:** The agent can pick either tool for the same request, risking broad reads.

**Fix:** State a selection boundary in both descriptions (e.g. list for filtered discovery, single-record tool for a known identifier) or merge into one find tool.

### High: T4 — mcp__naive_a__cancel_order

Required input(s) orderId have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_customer

Required input(s) name have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_invoice

Required input(s) orderId, amount have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_order

Required input(s) customerId, sku, quantity have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__create_product

Required input(s) sku, name, quantity have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__delete_customer

Required input(s) customerId have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_invoice_by_id

Required input(s) invoiceId have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_or_update_stock

Required input(s) sku have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_order_by_id

Required input(s) orderId have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__get_product_by_sku

Required input(s) sku have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__send_invoice

Required input(s) invoiceId have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__update_customer

Required input(s) customerId, fields have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__update_order

Required input(s) orderId, fields have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### High: T4 — mcp__naive_a__update_product

Required input(s) sku, fields have no meaningful description, format, constraint or example (at most a bare label such as 'Order ID').

**Why it matters:** The agent must guess identifier formats and free-form fields contents.

**Fix:** Document format, constraints and an example for each required property.

### Medium: C1 — all tools

Serialized definitions of the 20 tools total about 61091 UTF-8 bytes (~15273 estimated tokens, estimate only), mostly repeated boilerplate.

**Why it matters:** Large fixed context cost on every session.

**Fix:** Remove repeated boilerplate and consolidate tools.

### Medium: R2 — mcp__naive_a__get_order_by_id

Both order responses repeatedly include about seven internal/unrelated fields (internalRoute, warehouseBin, auditTag, sourceSystem, retryCounter, exportMarker, billingSegment) beyond what the status task needs.

**Why it matters:** Wasted context and exposure of internal data.; evidence: CALL-08, CALL-09

**Fix:** Return a compact user-facing projection with an opt-in detail mode.

### Medium: S1 — mcp__naive_a__cancel_order

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_customer

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_invoice

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_order

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__create_product

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__delete_customer

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__get_or_update_stock

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__send_invoice

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__update_customer

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__update_order

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S1 — mcp__naive_a__update_product

State-changing tool; no read-only/destructive annotations are visible to the model (whether the gap is at server or host is unknown).

**Why it matters:** The agent and host cannot gate mutation-capable tools.

**Fix:** Publish accurate readOnlyHint/destructiveHint/idempotentHint annotations.

### Medium: S4 — mcp__naive_a__create_customer

Create operation with no idempotency key in its schema.

**Why it matters:** A retry can create duplicate records.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: S4 — mcp__naive_a__create_invoice

Create operation with no idempotency key in its schema.

**Why it matters:** A retry can create duplicate records.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: S4 — mcp__naive_a__create_order

Create operation with no idempotency key in its schema.

**Why it matters:** A retry can create duplicate records.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: S4 — mcp__naive_a__create_product

Create operation with no idempotency key in its schema.

**Why it matters:** A retry can create duplicate records.

**Fix:** Require a client idempotency key and document retry behavior.

### Medium: T1 — all tools

The 20 tools mirror legacy CRUD endpoints one-to-one per entity (get/list/create/update/delete), described as direct endpoint wrappers.

**Why it matters:** Task-level work requires the agent to chain many endpoint calls.

**Fix:** Redesign around user tasks, e.g. find_account, prepare_order (preview), check_invoice_status.

### Medium: T3 — mcp__naive_a__cancel_order

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__create_customer

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__create_invoice

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__create_order

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__create_product

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__delete_customer

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__get_customer

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__get_invoice_by_id

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__get_or_update_stock

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__get_order_by_id

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__get_product_by_sku

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__list_customers

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__list_invoices

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__list_orders

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__list_products

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__list_stock

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__send_invoice

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__update_customer

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__update_order

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T3 — mcp__naive_a__update_product

Description is generic boilerplate; it says explicitly that it does not define which task should select the tool or its safe alternatives.

**Why it matters:** The agent lacks guidance on when to use or avoid the tool.

**Fix:** Describe the user task it serves, when to use it, and which tool to use instead.

### Medium: T5 — mcp__naive_a__cancel_order

Requires opaque orderId; list_orders filters only by fromDate/status and no tool looks up an order by readable order number or customer.

**Why it matters:** The agent cannot reliably obtain the identifier from a user-facing reference.

**Fix:** Add order lookup by order number/customer name returning the internal reference.

### Medium: T5 — mcp__naive_a__create_invoice

Requires opaque orderId; list_orders filters only by fromDate/status and no tool looks up an order by readable order number or customer.

**Why it matters:** The agent cannot reliably obtain the identifier from a user-facing reference.

**Fix:** Add order lookup by order number/customer name returning the internal reference.

### Medium: T5 — mcp__naive_a__get_invoice_by_id

Requires opaque invoiceId; list_invoices returns unlabeled IDs (no invoice number or customer) so there is no readable lookup path.

**Why it matters:** Invoice identification relies on guesswork.

**Fix:** Return invoice number and customer name from list_invoices and accept the invoice number.

### Medium: T5 — mcp__naive_a__get_order_by_id

Requires opaque orderId; list_orders filters only by fromDate/status and no tool looks up an order by readable order number or customer.

**Why it matters:** The agent cannot reliably obtain the identifier from a user-facing reference.

**Fix:** Add order lookup by order number/customer name returning the internal reference.

### Medium: T5 — mcp__naive_a__send_invoice

Requires opaque invoiceId; list_invoices returns unlabeled IDs (no invoice number or customer) so there is no readable lookup path.

**Why it matters:** Invoice identification relies on guesswork.

**Fix:** Return invoice number and customer name from list_invoices and accept the invoice number.

### Medium: T5 — mcp__naive_a__update_order

Requires opaque orderId; list_orders filters only by fromDate/status and no tool looks up an order by readable order number or customer.

**Why it matters:** The agent cannot reliably obtain the identifier from a user-facing reference.

**Fix:** Add order lookup by order number/customer name returning the internal reference.

### Low: R3 — mcp__naive_a__list_invoices

Invoice rows contain id, status, amount and currency but no invoice number or customer name.

**Why it matters:** Rows cannot be interpreted or matched to a customer without extra calls.; evidence: CALL-10, CALL-11

**Fix:** Include invoice_number and customer_name (and date) in rows.

## Not tested

- P3 skipped: No documented safe maximum page size on any list tool; unbounded request not allowed. R1 reported statically.
- P5 skipped: Write probes disabled; no write or destructive tool was called.

## Run details

- Environment: test
- Target: local synthetic wholesale test server (naive_a / naive_b)
- Agent/model: Claude Code / claude-sonnet-5-5
- Date: 2026-11-09
- Calls: 11
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent.

This is an automated design review, not a security audit.

Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.
