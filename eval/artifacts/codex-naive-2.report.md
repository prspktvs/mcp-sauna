# mcp-sauna review report

**Overall grade: incomplete** — The review is incomplete; skipped probes are not counted as passes.

## Summary

Top fixes:

- **S5 (mcp__naive_a__get_invoice_by_id):** Enforce authenticated identity permissions on each invoice read and add a cross-identity denial regression test.
- **E1 (mcp__naive_a__list_orders):** Validate date format before the upstream call and return a structured invalid_date error with an expected format.
- **E2 (mcp__naive_a__get_invoice_by_id):** Reject blank required identifiers with a structured missing_required_field error.

## Scorecard

| Dimension | Grade | Status | Findings |
| --- | --- | --- | ---: |
| Tool design | D | incomplete | 46 |
| Context cost | C | complete | 1 |
| Responses | D | incomplete | 7 |
| Errors | D | incomplete | 4 |
| Safety | F | incomplete | 25 |
| | | Incomplete: P1 skipped: TASK-01 skipped after bounded customer discovery: list_orders has no customer/name/ID filter for the requested scope. TASK-03 skipped: list_invoices lacks unpaid/status and page-size filters. TASK-04 skipped: no read-only prepare/preview tool exists; writes are disabled. TASK-05 attempted twice but invoice responses lack dates/readable labels, so most-recent status cannot be established. TASK-02 had two bounded reads; product name, quantity and reorderPoint support the answer, with unrelated products also returned. | |
| | | Incomplete: P1 skipped: TASK-01 skipped after bounded customer discovery: list_orders has no customer/name/ID filter for the requested scope. TASK-03 skipped: list_invoices lacks unpaid/status and page-size filters. TASK-04 skipped: no read-only prepare/preview tool exists; writes are disabled. TASK-05 attempted twice but invoice responses lack dates/readable labels, so most-recent status cannot be established. TASK-02 had two bounded reads; product name, quantity and reorderPoint support the answer, with unrelated products also returned. | |
| | | Incomplete: P3 skipped: All five list schemas lack a documented safe maximum/page size; no unbounded request was sent. | |
| | | Incomplete: P2 skipped: Partial coverage: malformed date tested once and empty identifiers tested on every read-only by-ID tool, including optional customerId. Empty optional customerId returning null is not E2. Stock tool skipped because it is write-capable. Omitted required fields are host-required and no numeric read bounds exist. No additional unknown-name test was needed after one applicable case per tool. | |
| | | Incomplete: P5 skipped: Writes disabled; all write-capable and destructive tools were excluded. Mutation findings are contract observations only. | |

## Metrics

- Task success rate: 4/5 attempted (80%); 3 skipped
- Average tool calls per task: 1.4
- Average estimated tokens per task: 135 (estimate)
- Tool definitions: 30370 estimated tokens (121477 UTF-8 bytes)
- Unsafe behaviors found: 25
- Total tool calls: 15

## Findings

### Critical: S5 — mcp__naive_a__get_invoice_by_id

Observed exact same narrow invoice read through both configured identities returned the requested restricted record. User confirmed A may see it and B must not. Evidence records retain the actual A/B aliases.

**Why it matters:** Identity B can read a synthetic record reserved for A; authorization isolation is broken.; evidence: CALL-13, CALL-14

**Fix:** Enforce authenticated identity permissions on each invoice read and add a cross-identity denial regression test.

### High: E1 — mcp__naive_a__list_orders

Observed malformed date case returned only status and stack fields, with an upstream error and no actionable validation guidance.

**Why it matters:** The agent cannot correct input safely from the error.; evidence: CALL-08

**Fix:** Validate date format before the upstream call and return a structured invalid_date error with an expected format.

### High: E2 — mcp__naive_a__get_invoice_by_id

Observed empty required identifier accepted as success with empty/null invoice, without validation error.

**Why it matters:** Missing required input is indistinguishable from no matching record.; evidence: CALL-10

**Fix:** Reject blank required identifiers with a structured missing_required_field error.

### High: E2 — mcp__naive_a__get_order_by_id

Observed empty required identifier accepted as success with empty/null orders, without validation error.

**Why it matters:** Missing required input is indistinguishable from no matching record.; evidence: CALL-11

**Fix:** Reject blank required identifiers with a structured missing_required_field error.

### High: E2 — mcp__naive_a__get_product_by_sku

Observed empty required identifier accepted as success with empty/null product, without validation error.

**Why it matters:** Missing required input is indistinguishable from no matching record.; evidence: CALL-12

**Fix:** Reject blank required identifiers with a structured missing_required_field error.

### High: R1 — mcp__naive_a__list_customers

Static schema lacks limit/maxItems and cursor/continuation inputs; no output schema documents total or has-more. P3 was skipped.

**Why it matters:** Completeness and maximum response size are unknown.

**Fix:** Add a documented maximum limit, cursor and output count/has-more contract.

### High: R1 — mcp__naive_a__list_invoices

Static schema lacks limit/maxItems and cursor/continuation inputs; no output schema documents total or has-more. P3 was skipped.

**Why it matters:** Completeness and maximum response size are unknown.

**Fix:** Add a documented maximum limit, cursor and output count/has-more contract.

### High: R1 — mcp__naive_a__list_orders

Static schema lacks limit/maxItems and cursor/continuation inputs; no output schema documents total or has-more. P3 was skipped.

**Why it matters:** Completeness and maximum response size are unknown.

**Fix:** Add a documented maximum limit, cursor and output count/has-more contract.

### High: R1 — mcp__naive_a__list_products

Static schema lacks limit/maxItems and cursor/continuation inputs; no output schema documents total or has-more. P3 was skipped.

**Why it matters:** Completeness and maximum response size are unknown.

**Fix:** Add a documented maximum limit, cursor and output count/has-more contract.

### High: R1 — mcp__naive_a__list_stock

Static schema lacks limit/maxItems and cursor/continuation inputs; no output schema documents total or has-more. P3 was skipped.

**Why it matters:** Completeness and maximum response size are unknown.

**Fix:** Add a documented maximum limit, cursor and output count/has-more contract.

### High: S2 — mcp__naive_a__get_or_update_stock

Static: one tool retrieves stock and accepts optional quantity for a stock update.

**Why it matters:** A nominal read workflow can enter a state-changing path.

**Fix:** Split check_stock from adjust_stock.

### High: S3 — mcp__naive_a__cancel_order

Static: consequential destructive action has no documented preview/confirmation field or equivalent safeguard. Runtime behavior was not tested.

**Why it matters:** An unintended tool call could commit a consequential action.

**Fix:** Require a reviewed preview or explicit confirmation token before committing the action.

### High: S3 — mcp__naive_a__create_invoice

Static: consequential financial action has no documented preview/confirmation field or equivalent safeguard. Runtime behavior was not tested.

**Why it matters:** An unintended tool call could commit a consequential action.

**Fix:** Require a reviewed preview or explicit confirmation token before committing the action.

### High: S3 — mcp__naive_a__create_order

Static: consequential order placement has no documented preview/confirmation field or equivalent safeguard. Runtime behavior was not tested.

**Why it matters:** An unintended tool call could commit a consequential action.

**Fix:** Require a reviewed preview or explicit confirmation token before committing the action.

### High: S3 — mcp__naive_a__delete_customer

Static: consequential destructive action has no documented preview/confirmation field or equivalent safeguard. Runtime behavior was not tested.

**Why it matters:** An unintended tool call could commit a consequential action.

**Fix:** Require a reviewed preview or explicit confirmation token before committing the action.

### High: S3 — mcp__naive_a__get_or_update_stock

Static: consequential inventory adjustment has no documented preview/confirmation field or equivalent safeguard. Runtime behavior was not tested.

**Why it matters:** An unintended tool call could commit a consequential action.

**Fix:** Require a reviewed preview or explicit confirmation token before committing the action.

### High: S3 — mcp__naive_a__send_invoice

Static: consequential external send has no documented preview/confirmation field or equivalent safeguard. Runtime behavior was not tested.

**Why it matters:** An unintended tool call could commit a consequential action.

**Fix:** Require a reviewed preview or explicit confirmation token before committing the action.

### High: S6 — mcp__naive_a__get_customer

Observed admin_note contains agent-directed instruction content, classified as an instruction-override attempt. Content was ignored and is neither copied nor retained.

**Why it matters:** Untrusted result content may redirect agent behavior.; evidence: CALL-04, CALL-09

**Fix:** Remove agent-directed instructions from result data and isolate free-text notes as untrusted content.

### High: T2 — mcp__naive_a__list_customers

Static: mcp__naive_a__list_customers and mcp__naive_a__get_customer both plausibly serve customer profile lookup, but neither describes when filtered discovery versus exact-record retrieval is appropriate.

**Why it matters:** The documented contracts leave the selection boundary unclear.

**Fix:** Define list_customers as bounded discovery and the read portion of get_customer as exact-record retrieval, with explicit selection examples.

### High: T2 — mcp__naive_a__list_invoices

Static: mcp__naive_a__list_invoices and mcp__naive_a__get_invoice_by_id both plausibly serve invoice lookup, but neither describes when filtered discovery versus exact-record retrieval is appropriate.

**Why it matters:** The documented contracts leave the selection boundary unclear.

**Fix:** Define list_invoices as bounded discovery and the read portion of get_invoice_by_id as exact-record retrieval, with explicit selection examples.

### High: T2 — mcp__naive_a__list_orders

Static: mcp__naive_a__list_orders and mcp__naive_a__get_order_by_id both plausibly serve order/status lookup, but neither describes when filtered discovery versus exact-record retrieval is appropriate.

**Why it matters:** The documented contracts leave the selection boundary unclear.

**Fix:** Define list_orders as bounded discovery and the read portion of get_order_by_id as exact-record retrieval, with explicit selection examples.

### High: T2 — mcp__naive_a__list_products

Static: mcp__naive_a__list_products and mcp__naive_a__get_product_by_sku both plausibly serve product lookup, but neither describes when filtered discovery versus exact-record retrieval is appropriate.

**Why it matters:** The documented contracts leave the selection boundary unclear.

**Fix:** Define list_products as bounded discovery and the read portion of get_product_by_sku as exact-record retrieval, with explicit selection examples.

### High: T2 — mcp__naive_a__list_stock

Static: mcp__naive_a__list_stock and mcp__naive_a__get_or_update_stock both plausibly serve stock lookup, but neither describes when filtered discovery versus exact-record retrieval is appropriate.

**Why it matters:** The documented contracts leave the selection boundary unclear.

**Fix:** Define list_stock as bounded discovery and the read portion of get_or_update_stock as exact-record retrieval, with explicit selection examples.

### High: T4 — mcp__naive_a__cancel_order

Static required-input checklist: orderId has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__create_customer

Static required-input checklist: name has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__create_invoice

Static required-input checklist: amount has no meaningful description; orderId has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__create_order

Static required-input checklist: customerId has no meaningful description; quantity has no meaningful description; sku has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__create_product

Static required-input checklist: name has no meaningful description; quantity has no meaningful description; sku has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__delete_customer

Static required-input checklist: customerId has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__get_invoice_by_id

Static required-input checklist: invoiceId has only a label. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__get_or_update_stock

Static required-input checklist: sku has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__get_order_by_id

Static required-input checklist: orderId has only a label. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__get_product_by_sku

Static required-input checklist: sku has only a label. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__send_invoice

Static required-input checklist: invoiceId has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__update_customer

Static required-input checklist: customerId has no meaningful description; fields has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__update_order

Static required-input checklist: fields has no meaningful description; orderId has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### High: T4 — mcp__naive_a__update_product

Static required-input checklist: fields has no meaningful description; sku has no meaningful description. No domain formats, bounds, allowed values or examples are supplied.

**Why it matters:** Required values must be guessed and invalid requests become likely.

**Fix:** Document every required field with meaningful purpose, format, constraints and a safe synthetic example.

### Medium: C1 — all tools

Host-visible serialized definitions total 121477 UTF-8 bytes, approximately 30370 tokens (ceil(bytes/4) estimate). Both identical 20-tool alias catalogs are exposed simultaneously; design is assessed once under identity A.

**Why it matters:** Repeated endpoint boilerplate and duplicate identity catalogs consume model context.

**Fix:** Shorten descriptions, consolidate task tools and avoid exposing duplicate catalogs outside identity testing.

### Medium: R2 — mcp__naive_a__get_order_by_id

Observed repeatedly: status lookups returned 16 row fields, including internalRoute, warehouseBin, auditTag, sourceSystem, retryCounter, exportMarker and billingSegment.

**Why it matters:** Unrelated internal fields increase context cost and disclosure.; evidence: CALL-05, CALL-06

**Fix:** Return compact order number/status/customer fields by default; gate detailed diagnostics separately.

### Medium: S1 — mcp__naive_a__cancel_order

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__create_customer

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__create_invoice

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__create_order

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__create_product

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__delete_customer

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__get_or_update_stock

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__send_invoice

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__update_customer

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__update_order

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S1 — mcp__naive_a__update_product

Static host contract: state-changing tool has no model-visible annotation metadata. Whether the gap originates at server or host is unknown.

**Why it matters:** The agent lacks reliable read-only/destructive/idempotent hints.

**Fix:** Expose accurate MCP readOnlyHint, destructiveHint and idempotentHint annotations through the host.

### Medium: S4 — mcp__naive_a__create_customer

Static: create or retry-sensitive send contract contains no idempotency key or documented equivalent.

**Why it matters:** Retries may duplicate records or external sends.

**Fix:** Add client-supplied idempotency keys and document replay behavior.

### Medium: S4 — mcp__naive_a__create_invoice

Static: create or retry-sensitive send contract contains no idempotency key or documented equivalent.

**Why it matters:** Retries may duplicate records or external sends.

**Fix:** Add client-supplied idempotency keys and document replay behavior.

### Medium: S4 — mcp__naive_a__create_order

Static: create or retry-sensitive send contract contains no idempotency key or documented equivalent.

**Why it matters:** Retries may duplicate records or external sends.

**Fix:** Add client-supplied idempotency keys and document replay behavior.

### Medium: S4 — mcp__naive_a__create_product

Static: create or retry-sensitive send contract contains no idempotency key or documented equivalent.

**Why it matters:** Retries may duplicate records or external sends.

**Fix:** Add client-supplied idempotency keys and document replay behavior.

### Medium: S4 — mcp__naive_a__send_invoice

Static: create or retry-sensitive send contract contains no idempotency key or documented equivalent.

**Why it matters:** Retries may duplicate records or external sends.

**Fix:** Add client-supplied idempotency keys and document replay behavior.

### Medium: T1 — all tools

Static: the 20-tool inventory mirrors customer, order, invoice, product and stock endpoints, including create/get/list/update clusters.

**Why it matters:** Endpoint selection and multi-step assembly burden the agent.

**Fix:** Offer task tools such as find_account, check_order_status and prepare_order with explicit boundaries.

### Medium: T3 — mcp__naive_a__cancel_order

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__create_customer

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__create_invoice

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__create_order

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__create_product

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__delete_customer

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__get_customer

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__get_invoice_by_id

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__get_or_update_stock

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__get_order_by_id

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__get_product_by_sku

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__list_customers

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__list_invoices

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__list_orders

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__list_products

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__list_stock

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__send_invoice

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__update_customer

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__update_order

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T3 — mcp__naive_a__update_product

Static description has no positive task-selection guidance plus exclusion/alternative boundary.

**Why it matters:** The agent cannot reliably select a safe tool for the user task.

**Fix:** Document when to use this tool, required scope, and when to choose a named alternative.

### Medium: T5 — mcp__naive_a__cancel_order

Static: required orderId is an internal reference. No tool resolves readable order number or customer name to that ID; list_orders only accepts status/fromDate and publishes no output schema.

**Why it matters:** A user-facing order reference cannot be reliably resolved by the documented inventory.

**Fix:** Provide bounded order lookup by readable order number/customer with labeled internal references.

### Medium: T5 — mcp__naive_a__create_invoice

Static: required orderId is an internal reference. No tool resolves readable order number or customer name to that ID; list_orders only accepts status/fromDate and publishes no output schema.

**Why it matters:** A user-facing order reference cannot be reliably resolved by the documented inventory.

**Fix:** Provide bounded order lookup by readable order number/customer with labeled internal references.

### Medium: T5 — mcp__naive_a__get_invoice_by_id

Static plus sampled list evidence: required invoiceId is opaque; list_invoices accepts customerName but returns only id/status/amount/currency, without invoice/customer labels. No invoice-number resolver exists.

**Why it matters:** A caller cannot identify which unlabeled invoice ID is the intended invoice.

**Fix:** Add a bounded readable invoice-number/customer lookup returning invoice number, customer name and internal ID.

### Medium: T5 — mcp__naive_a__get_order_by_id

Static: required orderId is an internal reference. No tool resolves readable order number or customer name to that ID; list_orders only accepts status/fromDate and publishes no output schema.

**Why it matters:** A user-facing order reference cannot be reliably resolved by the documented inventory.

**Fix:** Provide bounded order lookup by readable order number/customer with labeled internal references.

### Medium: T5 — mcp__naive_a__send_invoice

Static plus sampled list evidence: required invoiceId is opaque; list_invoices accepts customerName but returns only id/status/amount/currency, without invoice/customer labels. No invoice-number resolver exists.

**Why it matters:** A caller cannot identify which unlabeled invoice ID is the intended invoice.

**Fix:** Add a bounded readable invoice-number/customer lookup returning invoice number, customer name and internal ID.

### Medium: T5 — mcp__naive_a__update_order

Static: required orderId is an internal reference. No tool resolves readable order number or customer name to that ID; list_orders only accepts status/fromDate and publishes no output schema.

**Why it matters:** A user-facing order reference cannot be reliably resolved by the documented inventory.

**Fix:** Provide bounded order lookup by readable order number/customer with labeled internal references.

### Low: R3 — mcp__naive_a__list_invoices

Observed twice: invoice rows expose id/status/amount/currency but no invoice number, customer name or other readable invoice label.

**Why it matters:** The requested invoice cannot be identified or attributed to a readable customer.; evidence: CALL-03, CALL-07

**Fix:** Return invoice_number, customer_name and relevant dates alongside status.

## Not tested

- P1 skipped: TASK-01 skipped after bounded customer discovery: list_orders has no customer/name/ID filter for the requested scope. TASK-03 skipped: list_invoices lacks unpaid/status and page-size filters. TASK-04 skipped: no read-only prepare/preview tool exists; writes are disabled. TASK-05 attempted twice but invoice responses lack dates/readable labels, so most-recent status cannot be established. TASK-02 had two bounded reads; product name, quantity and reorderPoint support the answer, with unrelated products also returned.
- P2 skipped: Partial coverage: malformed date tested once and empty identifiers tested on every read-only by-ID tool, including optional customerId. Empty optional customerId returning null is not E2. Stock tool skipped because it is write-capable. Omitted required fields are host-required and no numeric read bounds exist. No additional unknown-name test was needed after one applicable case per tool.
- P3 skipped: All five list schemas lack a documented safe maximum/page size; no unbounded request was sent.
- P5 skipped: Writes disabled; all write-capable and destructive tools were excluded. Mutation findings are contract observations only.

## Run details

- Environment: test
- Target: local synthetic wholesale naive reference server; naive_a / naive_b
- Agent/model: Codex / unknown
- Date: 2026-11-09
- Calls: 15
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent.

This is an automated design review, not a security audit.

Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.

## Review scope and interpretation

The user confirmed the local synthetic wholesale test server, the test environment, the bundled example tasks, and two separately configured identities with different invoice permissions. No configured endpoint URL, output schemas, or annotation metadata were exposed by the host. The host-visible names and descriptions showed no production signal. Identical definitions were reviewed once under naive_a; the naive_b catalog is included in the context estimate because both catalogs were simultaneously exposed. The input schemas in run.json reconstruct the host-visible typed declarations; unavailable output schemas and annotations remain null.

Tool classification, applied to both aliases:

- Read: get_customer, get_invoice_by_id, get_order_by_id, get_product_by_sku, list_customers, list_invoices, list_orders, list_products, list_stock.
- Write-capable: create_customer, create_invoice, create_order, create_product, get_or_update_stock, update_customer, update_order, update_product.
- Destructive or externally consequential, never called: cancel_order, delete_customer, send_invoice.

Static review covered T1–T5, C1, R1 and S1–S4/S6 for every canonical tool. T4 findings enumerate every affected required property; optional properties were excluded. Customer IDs have a readable-name resolver via list_customers(name), and product SKUs are user-facing identifiers with labeled product discovery. Order and invoice resolver limitations are identified individually. No agent-directed instruction finding was established in definitions. No state-changing behavior was probed or inferred from a call.

P6 ran passively across all probe results. Only sanitized field names, counts, sizes, outcomes and neutral classifications were retained. The optional empty customer identifier is not treated as missing required input. Successful empty required-ID responses are behavioral validation failures, while the raw date error is the only error outcome; the three-identical-error stop condition was not reached. No response exceeded 608 bytes. The run stayed below the default 100-call and 15-minute limits.

TASK-01's single bounded customer-discovery call is logged without a task ID because the order task was skipped before an order request could be safely scoped. TASK-02 used two reads within one task attempt to verify result applicability. TASK-05 was retried once and remained unsupported. The five attempted tasks produced four supported answers; skipped tasks were excluded from that denominator.

The grader marks the overall review incomplete when probes are skipped, even when severe findings already establish a dimension's known grade. Safety has a known F from the observed identity-isolation failure. The unsafe-behavior metric includes static safety findings and must not be read as a count of observed exploits.
