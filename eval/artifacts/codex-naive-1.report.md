# mcp-sauna review report

Review scope: local synthetic wholesale server, environment `test`, two user-confirmed configured identities. No configured endpoint URL was visible; names and exposed definitions showed no production signal. Both catalogs have identical definitions, so design findings use identity A's exact host alias once. Both catalogs are exposed together and count toward context cost. No write, destructive, mixed-effect stock, unfiltered list, or unbounded pagination call was made. Defaults remained 15 minutes and 100 calls; 14 target calls were made.

Evidence limitations: input schemas were reconstructed from the host's typed declarations; original JSON Schema constraints, annotations and output schemas were not exposed. Null metadata means unknown, rather than proof the server omitted it. The context estimate measures the compact normalized definitions, not a tokenizer-exact count. Static mutation risks are contract findings, not demonstrated mutation behavior. The grader's “unsafe behaviors found” metric counts all S-rule findings, including static ones.

Probe accounting: P1 attempted five tasks, with four supported and one unresolved after retry; three tasks were skipped. P2 tested one malformed date and empty identifiers on all four read-by-ID tools, including the optional customer identifier (not counted as E2). P4 used exactly the same invoice read through A and B and observed disclosure to B. P6 passively inspected definitions and results; instruction content was not followed or copied. P3 and P5 were skipped.

CALL-01 completed a filtered server read, but local metadata instrumentation failed before retaining its response. Zero size/item fields denote unavailable measurements for this call only, not an empty server response. The same filtered task was retried once as CALL-02; its measurements were retained. No instrumentation failure is treated as a server error finding. Response token estimates cover serialized host envelopes and exclude assistant reasoning. All saved probe evidence consists of sanitized metadata; no argument or result values are retained.

**Overall grade: incomplete** — The review is incomplete; skipped probes are not counted as passes.

## Summary

Top fixes:

- **S5 (mcp__naive_a__get_invoice_by_id):** Enforce per-identity authorization before returning any invoice fields.
- **E1 (mcp__naive_a__list_orders):** Validate the date and return a structured field error with format guidance.
- **E2 (mcp__naive_a__get_invoice_by_id):** Reject empty required identifiers with actionable validation errors.

## Scorecard

| Dimension | Grade | Status | Findings |
| --- | --- | --- | ---: |
| Tool design | D | incomplete | 46 |
| Context cost | C | complete | 1 |
| Responses | D | incomplete | 7 |
| Errors | D | incomplete | 4 |
| Safety | F | incomplete | 25 |
| | | Incomplete: P1 skipped: TASK-01: no customer filter on orders. TASK-03: no unpaid filter or five-item cap. TASK-04: no heater-name filter or safe preview tool; writes disabled. TASK-05 attempted twice but no date/order metadata establishes most recent invoice. | |
| | | Incomplete: P1 skipped: TASK-01: no customer filter on orders. TASK-03: no unpaid filter or five-item cap. TASK-04: no heater-name filter or safe preview tool; writes disabled. TASK-05 attempted twice but no date/order metadata establishes most recent invoice. | |
| | | Incomplete: P3 skipped: All five list schemas lack a documented maximum page size; no unbounded behavioral request made. | |
| | | Incomplete: P2 skipped: Unknown-readable-name case has no confirmed test fixture. Missing required fields are blocked by host types; no numeric bounded read input exists. Empty optional customer ID was tested but is not E2 evidence. Mixed stock read/write tool was excluded. | |
| | | Incomplete: P5 skipped: Write probes disabled; no mutation or destructive tools called. | |

## Metrics

- Task success rate: 4/5 attempted (80%); 3 skipped
- Average tool calls per task: 1.4
- Average estimated tokens per task: 114 (estimate)
- Tool definitions: 30331 estimated tokens (121321 UTF-8 bytes)
- Unsafe behaviors found: 25
- Total tool calls: 14

## Findings

### Critical: S5 — mcp__naive_a__get_invoice_by_id

The exact same restricted-record read returned record fields to both configured identities despite the confirmed denial expectation for B.

**Why it matters:** Observed cross-identity disclosure violates the stated access boundary.; evidence: CALL-13, CALL-14

**Fix:** Enforce per-identity authorization before returning any invoice fields.

### High: E1 — mcp__naive_a__list_orders

Malformed date filter returned only status and stack fields, without actionable validation guidance.

**Why it matters:** The caller cannot safely correct the request.; evidence: CALL-08

**Fix:** Validate the date and return a structured field error with format guidance.

### High: E2 — mcp__naive_a__get_invoice_by_id

Empty required identifier was accepted and returned a successful null/empty record response.

**Why it matters:** Missing input is indistinguishable from no match.; evidence: CALL-09

**Fix:** Reject empty required identifiers with actionable validation errors.

### High: E2 — mcp__naive_a__get_order_by_id

Empty required identifier was accepted and returned a successful null/empty record response.

**Why it matters:** Missing input is indistinguishable from no match.; evidence: CALL-10

**Fix:** Reject empty required identifiers with actionable validation errors.

### High: E2 — mcp__naive_a__get_product_by_sku

Empty required identifier was accepted and returned a successful null/empty record response.

**Why it matters:** Missing input is indistinguishable from no match.; evidence: CALL-11

**Fix:** Reject empty required identifiers with actionable validation errors.

### High: R1 — mcp__naive_a__list_customers

Static schema exposes no cap or continuation input; no output schema documents total/has-more. P3 was skipped.

**Why it matters:** Completeness and context usage are unbounded by contract.

**Fix:** Add a capped limit, cursor and documented total/has-more output.

### High: R1 — mcp__naive_a__list_invoices

Static schema exposes no cap or continuation input; no output schema documents total/has-more. P3 was skipped.

**Why it matters:** Completeness and context usage are unbounded by contract.

**Fix:** Add a capped limit, cursor and documented total/has-more output.

### High: R1 — mcp__naive_a__list_orders

Static schema exposes no cap or continuation input; no output schema documents total/has-more. P3 was skipped.

**Why it matters:** Completeness and context usage are unbounded by contract.

**Fix:** Add a capped limit, cursor and documented total/has-more output.

### High: R1 — mcp__naive_a__list_products

Static schema exposes no cap or continuation input; no output schema documents total/has-more. P3 was skipped.

**Why it matters:** Completeness and context usage are unbounded by contract.

**Fix:** Add a capped limit, cursor and documented total/has-more output.

### High: R1 — mcp__naive_a__list_stock

Static schema exposes no cap or continuation input; no output schema documents total/has-more. P3 was skipped.

**Why it matters:** Completeness and context usage are unbounded by contract.

**Fix:** Add a capped limit, cursor and documented total/has-more output.

### High: S2 — mcp__naive_a__get_or_update_stock

Static quantity argument switches the same tool between reading and changing inventory.

**Why it matters:** An apparent stock lookup can mutate state.

**Fix:** Split stock reads and adjustments.

### High: S3 — mcp__naive_a__cancel_order

Static consequential mutation contract has no documented preview or confirmation safeguard; behavior was not probed.

**Why it matters:** An unintended call can commit a consequential action.

**Fix:** Require a reviewed preview and explicit confirmation before committing.

### High: S3 — mcp__naive_a__create_invoice

Static consequential mutation contract has no documented preview or confirmation safeguard; behavior was not probed.

**Why it matters:** An unintended call can commit a consequential action.

**Fix:** Require a reviewed preview and explicit confirmation before committing.

### High: S3 — mcp__naive_a__create_order

Static consequential mutation contract has no documented preview or confirmation safeguard; behavior was not probed.

**Why it matters:** An unintended call can commit a consequential action.

**Fix:** Require a reviewed preview and explicit confirmation before committing.

### High: S3 — mcp__naive_a__delete_customer

Static consequential mutation contract has no documented preview or confirmation safeguard; behavior was not probed.

**Why it matters:** An unintended call can commit a consequential action.

**Fix:** Require a reviewed preview and explicit confirmation before committing.

### High: S3 — mcp__naive_a__get_or_update_stock

Static consequential mutation contract has no documented preview or confirmation safeguard; behavior was not probed.

**Why it matters:** An unintended call can commit a consequential action.

**Fix:** Require a reviewed preview and explicit confirmation before committing.

### High: S3 — mcp__naive_a__send_invoice

Static consequential mutation contract has no documented preview or confirmation safeguard; behavior was not probed.

**Why it matters:** An unintended call can commit a consequential action.

**Fix:** Require a reviewed preview and explicit confirmation before committing.

### High: S6 — mcp__naive_a__get_customer

Observed agent-directed instruction content in admin_note; classified as an unrelated instruction attempt. Content was neither followed nor reproduced.

**Why it matters:** Untrusted record content can attempt to redirect agent behavior.; evidence: CALL-04, CALL-12

**Fix:** Remove agent instructions from record fields and keep retrieved content explicitly untrusted.

### High: T2 — mcp__naive_a__list_customers

Static: mcp__naive_a__list_customers and mcp__naive_a__get_customer both support entity lookup without explaining when broad/filter lookup versus a single-record read is appropriate.

**Why it matters:** Overlapping lookup scope encourages unsafe or wasteful tool selection.

**Fix:** Document resolution-versus-detail boundaries and safe filters.

### High: T2 — mcp__naive_a__list_invoices

Static: mcp__naive_a__list_invoices and mcp__naive_a__get_invoice_by_id both support entity lookup without explaining when broad/filter lookup versus a single-record read is appropriate.

**Why it matters:** Overlapping lookup scope encourages unsafe or wasteful tool selection.

**Fix:** Document resolution-versus-detail boundaries and safe filters.

### High: T2 — mcp__naive_a__list_orders

Static: mcp__naive_a__list_orders and mcp__naive_a__get_order_by_id both support entity lookup without explaining when broad/filter lookup versus a single-record read is appropriate.

**Why it matters:** Overlapping lookup scope encourages unsafe or wasteful tool selection.

**Fix:** Document resolution-versus-detail boundaries and safe filters.

### High: T2 — mcp__naive_a__list_products

Static: mcp__naive_a__list_products and mcp__naive_a__get_product_by_sku both support entity lookup without explaining when broad/filter lookup versus a single-record read is appropriate.

**Why it matters:** Overlapping lookup scope encourages unsafe or wasteful tool selection.

**Fix:** Document resolution-versus-detail boundaries and safe filters.

### High: T2 — mcp__naive_a__list_stock

Static: mcp__naive_a__list_stock and mcp__naive_a__get_or_update_stock both support entity lookup without explaining when broad/filter lookup versus a single-record read is appropriate.

**Why it matters:** Overlapping lookup scope encourages unsafe or wasteful tool selection.

**Fix:** Document resolution-versus-detail boundaries and safe filters.

### High: T4 — mcp__naive_a__cancel_order

Static required-input checklist: orderId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__create_customer

Static required-input checklist: name. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__create_invoice

Static required-input checklist: amount, orderId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__create_order

Static required-input checklist: customerId, quantity, sku. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__create_product

Static required-input checklist: name, quantity, sku. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__delete_customer

Static required-input checklist: customerId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__get_invoice_by_id

Static required-input checklist: invoiceId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__get_or_update_stock

Static required-input checklist: sku. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__get_order_by_id

Static required-input checklist: orderId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__get_product_by_sku

Static required-input checklist: sku. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__send_invoice

Static required-input checklist: invoiceId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__update_customer

Static required-input checklist: customerId, fields. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__update_order

Static required-input checklist: fields, orderId. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### High: T4 — mcp__naive_a__update_product

Static required-input checklist: fields, sku. Descriptions are absent or label-only; meaningful formats, constraints and examples are not exposed.

**Why it matters:** Required inputs cannot reliably be constructed.

**Fix:** Document every listed required field, domain formats, units, ranges, allowed values and examples.

### Medium: C1 — all tools

Static: both identical catalogs are exposed simultaneously. Normalized visible definitions serialize to 121321 UTF-8 bytes, approximately 30331 tokens (ceil(bytes/4)); input schemas reconstructed from host type declarations.

**Why it matters:** Repeated verbose definitions consume substantial model context.

**Fix:** Shorten descriptions and expose only the needed identity catalog.

### Medium: R2 — mcp__naive_a__get_order_by_id

Repeated status reads include internalRoute, warehouseBin, auditTag, sourceSystem, retryCounter, exportMarker and billingSegment among 16 row fields.

**Why it matters:** Unrelated internal fields add context cost and exposure.; evidence: CALL-05, CALL-06

**Fix:** Return status-focused summaries; opt into expanded details.

### Medium: S1 — mcp__naive_a__cancel_order

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__create_customer

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__create_invoice

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__create_order

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__create_product

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__delete_customer

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__get_or_update_stock

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__send_invoice

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__update_customer

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__update_order

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S1 — mcp__naive_a__update_product

Static agent-visible contract exposes no mutation annotations. Whether the server or host omitted them is unknown.

**Why it matters:** The agent lacks machine-readable effect hints.

**Fix:** Expose accurate readOnlyHint, destructiveHint and idempotentHint metadata through the host.

### Medium: S4 — mcp__naive_a__create_customer

Static retry-sensitive create/send contract has no documented idempotency mechanism.

**Why it matters:** Retries may duplicate logical effects.

**Fix:** Accept an idempotency key and document replay behavior.

### Medium: S4 — mcp__naive_a__create_invoice

Static retry-sensitive create/send contract has no documented idempotency mechanism.

**Why it matters:** Retries may duplicate logical effects.

**Fix:** Accept an idempotency key and document replay behavior.

### Medium: S4 — mcp__naive_a__create_order

Static retry-sensitive create/send contract has no documented idempotency mechanism.

**Why it matters:** Retries may duplicate logical effects.

**Fix:** Accept an idempotency key and document replay behavior.

### Medium: S4 — mcp__naive_a__create_product

Static retry-sensitive create/send contract has no documented idempotency mechanism.

**Why it matters:** Retries may duplicate logical effects.

**Fix:** Accept an idempotency key and document replay behavior.

### Medium: S4 — mcp__naive_a__send_invoice

Static retry-sensitive create/send contract has no documented idempotency mechanism.

**Why it matters:** Retries may duplicate logical effects.

**Fix:** Accept an idempotency key and document replay behavior.

### Medium: T1 — all tools

Static: the customer, product, order and invoice CRUD cluster mirrors upstream endpoints without end-user task boundaries.

**Why it matters:** Agents must assemble workflows from low-level endpoints.

**Fix:** Provide task tools for account resolution, order status, order preparation and invoice lookup.

### Medium: T3 — mcp__naive_a__cancel_order

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__create_customer

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__create_invoice

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__create_order

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__create_product

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__delete_customer

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__get_customer

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__get_invoice_by_id

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__get_or_update_stock

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__get_order_by_id

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__get_product_by_sku

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__list_customers

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__list_invoices

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__list_orders

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__list_products

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__list_stock

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__send_invoice

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__update_customer

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__update_order

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T3 — mcp__naive_a__update_product

Static description has no meaningful use/exclusion or alternative-selection boundary.

**Why it matters:** Tool choice depends on guesswork.

**Fix:** Document a concrete use case, exclusions, and the appropriate alternative.

### Medium: T5 — mcp__naive_a__cancel_order

Required orderId is opaque. The complete inventory has no readable invoice/order-number resolver; invoice list samples expose unlabeled internal IDs.

**Why it matters:** A readable user request cannot reliably supply the required internal reference.

**Fix:** Provide a readable-number/name resolver returning labeled internal references.

### Medium: T5 — mcp__naive_a__create_invoice

Required orderId is opaque. The complete inventory has no readable invoice/order-number resolver; invoice list samples expose unlabeled internal IDs.

**Why it matters:** A readable user request cannot reliably supply the required internal reference.

**Fix:** Provide a readable-number/name resolver returning labeled internal references.

### Medium: T5 — mcp__naive_a__get_invoice_by_id

Required invoiceId is opaque. The complete inventory has no readable invoice/order-number resolver; invoice list samples expose unlabeled internal IDs.

**Why it matters:** A readable user request cannot reliably supply the required internal reference.

**Fix:** Provide a readable-number/name resolver returning labeled internal references.

### Medium: T5 — mcp__naive_a__get_order_by_id

Required orderId is opaque. The complete inventory has no readable invoice/order-number resolver; invoice list samples expose unlabeled internal IDs.

**Why it matters:** A readable user request cannot reliably supply the required internal reference.

**Fix:** Provide a readable-number/name resolver returning labeled internal references.

### Medium: T5 — mcp__naive_a__send_invoice

Required invoiceId is opaque. The complete inventory has no readable invoice/order-number resolver; invoice list samples expose unlabeled internal IDs.

**Why it matters:** A readable user request cannot reliably supply the required internal reference.

**Fix:** Provide a readable-number/name resolver returning labeled internal references.

### Medium: T5 — mcp__naive_a__update_order

Required orderId is opaque. The complete inventory has no readable invoice/order-number resolver; invoice list samples expose unlabeled internal IDs.

**Why it matters:** A readable user request cannot reliably supply the required internal reference.

**Fix:** Provide a readable-number/name resolver returning labeled internal references.

### Low: R3 — mcp__naive_a__list_invoices

Sample invoice rows expose id, status, amount and currency without readable invoice/customer labels.

**Why it matters:** The user cannot interpret the opaque invoice references.; evidence: CALL-03, CALL-07

**Fix:** Return invoice number and readable customer name.

## Not tested

- P1 skipped: TASK-01: no customer filter on orders. TASK-03: no unpaid filter or five-item cap. TASK-04: no heater-name filter or safe preview tool; writes disabled. TASK-05 attempted twice but no date/order metadata establishes most recent invoice.
- P2 skipped: Unknown-readable-name case has no confirmed test fixture. Missing required fields are blocked by host types; no numeric bounded read input exists. Empty optional customer ID was tested but is not E2 evidence. Mixed stock read/write tool was excluded.
- P3 skipped: All five list schemas lack a documented maximum page size; no unbounded behavioral request made.
- P5 skipped: Write probes disabled; no mutation or destructive tools called.

## Run details

- Environment: test
- Target: local synthetic wholesale reference server; naive_a / naive_b
- Agent/model: Codex / unknown
- Date: 2026-11-09
- Calls: 14
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent.

This is an automated design review, not a security audit.

Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.
