# mcp-sauna review report

**Overall grade: incomplete** — The review is incomplete; skipped probes are not counted as passes.

## Summary

Top fixes:

- **S1 (mcp__good_a__place_order):** Expose accurate placement annotations to the model through the server and host: readOnlyHint false, with destructiveHint and idempotentHint matching the actual placement and exact-retry behavior.

## Scorecard

| Dimension | Grade | Status | Findings |
| --- | --- | --- | ---: |
| Tool design | A | incomplete | 0 |
| Context cost | A | complete | 0 |
| Responses | A | incomplete | 0 |
| Errors | A | incomplete | 0 |
| Safety | C | incomplete | 1 |
| | | Incomplete: P1 skipped: Partial: TASK-04 skipped because preview persistence is unknown, so it is conservatively classified write and writes are disabled. TASK-06 skipped because find_account accepts readable names, with no documented customer-ID resolver. TASK-05, TASK-07 and TASK-08 had no matching records after one retry each; no E2 inference from valid empty results. | |
| | | Incomplete: P1 skipped: Partial: TASK-04 skipped because preview persistence is unknown, so it is conservatively classified write and writes are disabled. TASK-06 skipped because find_account accepts readable names, with no documented customer-ID resolver. TASK-05, TASK-07 and TASK-08 had no matching records after one retry each; no E2 inference from valid empty results. | |
| | | Incomplete: P2 skipped: Partial: supported narrow malformed-date validation was observed. The host rejected an out-of-range limit before server execution; no validation bypass was attempted. Omitted required fields, wrong types and enum violations were not forced. No dedicated read-by-ID/SKU-only contract was exposed; empty optional filters were not tested. | |
| | | Incomplete: P5 skipped: All write probes disabled by the user. preview_order conservatively classified write because persistence is unspecified; place_order classified consequential write. Neither was invoked. Preview enforcement and idempotency remain behaviorally untested. | |

## Metrics

- Task success rate: 3/6 attempted (50%); 2 skipped
- Average tool calls per task: 2.0
- Average estimated tokens per task: 193 (estimate)
- Tool definitions: 2628 estimated tokens (10511 UTF-8 bytes)
- Unsafe behaviors found: 1
- Total tool calls: 17

## Findings

### Medium: S1 — mcp__good_a__place_order

Static, agent-visible contract limitation: place_order clearly changes state, but the host exposes no mutation annotations for either alias. Whether the gap originates at the server or host is unknown.

**Why it matters:** The agent cannot inspect readOnlyHint, destructiveHint, or idempotentHint to help classify placement. The reviewed-preview and confirmation boundaries remain documented.

**Fix:** Expose accurate placement annotations to the model through the server and host: readOnlyHint false, with destructiveHint and idempotentHint matching the actual placement and exact-retry behavior.

## Not tested

- P1 skipped: Partial: TASK-04 skipped because preview persistence is unknown, so it is conservatively classified write and writes are disabled. TASK-06 skipped because find_account accepts readable names, with no documented customer-ID resolver. TASK-05, TASK-07 and TASK-08 had no matching records after one retry each; no E2 inference from valid empty results.
- P2 skipped: Partial: supported narrow malformed-date validation was observed. The host rejected an out-of-range limit before server execution; no validation bypass was attempted. Omitted required fields, wrong types and enum violations were not forced. No dedicated read-by-ID/SKU-only contract was exposed; empty optional filters were not tested.
- P5 skipped: All write probes disabled by the user. preview_order conservatively classified write because persistence is unspecified; place_order classified consequential write. Neither was invoked. Preview enforcement and idempotency remain behaviorally untested.

## Run details

- Environment: test
- Target: Local synthetic reference server: good_a (A), good_b (B); identical design, two configured identities
- Agent/model: Codex / unknown
- Date: 2026-11-09
- Calls: 17
- Skill version: 0.1.0

Tool output passed through the model provider already used by the agent.

This is an automated design review, not a security audit.

Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.

## Scope, evidence, and limits

The user confirmed the bundled example tasks, the test environment, two separately configured identities, and their unequal access policy. No endpoint URL was visible; the exposed names and definitions contained no production signal. The review stayed within the default 15-minute and 100-call bounds. Only these three report artifacts were written. No write or destructive tool was called, and no unfiltered list/search call was made.

Both catalogs were simultaneously exposed to the model. Their six logical definitions are identical apart from identity aliases. Design findings use identity A's alias; call entries retain the actual alias. The context metric includes all twelve exposed aliases. It measures the serialized host-visible definition projections, including signatures and parameter comments, at 10,511 UTF-8 bytes and approximately 2,628 tokens using ceil(bytes / 4). Native JSON input/output schemas and annotation objects were unavailable; null schema fields in run.json denote unavailable native metadata, not tools with no inputs. The visible signatures were reviewed in full. This is not a tokenizer-exact or native-server-catalog measurement.

### Classification and static coverage

| Canonical tool (good_a; same design on good_b) | Classification | Required-property review |
| --- | --- | --- |
| check_stock | Read | product: readable product name or SKU, with example |
| find_account | Read | name: legal or trading name, with example |
| search_orders | Read | No required properties; optional query, date, limit and cursor documented |
| search_invoices | Read | No required properties; optional query, status, limit and cursor documented |
| preview_order | Write conservatively; persistence unknown | customer: readable name and example; quantity: whole units with bounds; sku: format example |
| place_order | Consequential write | confirmation: fixed approved value; idempotencyKey: minimum length and exact-retry guidance; previewId: preview_order source and example |

T1: this is a small task-oriented inventory rather than a CRUD cluster. T2: all fifteen distinct canonical pairs were considered. Account resolution, invoice search, order search and stock lookup serve distinct requests. Existing-order search, draft calculation and placement have explicit selection boundaries; shared subject matter does not establish overlap. T3: each definition gives a positive use case and an exclusion. T4: every required property is listed above; no underdocumentation finding was established. T5: the opaque required previewId has the documented preview_order resolver; SKU can be obtained through readable product lookup, and idempotencyKey is client-generated.

R1: both list/search contracts document a maximum page size and continuation input. Their observed responses supplied count and nextCursor. The stock/account tools are scoped readable-entity lookups rather than broad list interfaces. S1: the visible placement annotation limitation is the sole static finding; no claim is made about unseen server annotations. S2: no combined lookup/update operation was established. S3 and S4: placement documents reviewed-preview confirmation and exact-retry idempotency; their runtime enforcement remains untested. Preview persistence and retry sensitivity are unknown, so no mutation or idempotency defect was inferred for that tool. S6: passive inspection of both catalogs and retained probe observations found no agent-directed unrelated instructions. No result text was followed as instructions.

### Behavioral evidence

| Probe | Evidence and assessment |
| --- | --- |
| P1 / TASK-01 | CALL-01 had a local result-processing failure, followed by CALL-02. CALL-12's complete filtered page supports determining the most recent order from createdAt; first-page order alone did not establish recency. Three calls across two task attempts, including the shared P3 call. |
| P1 / TASK-02 | CALL-03 had no matches; the single retry CALL-04 returned one named product with quantity and reorderPoint, supporting the stock assessment. |
| P1 / TASK-03 | CALL-05 returned one matching invoice with a readable customer name and an exhausted continuation signal. Fewer matches than the requested first page is a valid result. |
| P1 / TASK-05, TASK-07, TASK-08 | CALL-06 through CALL-11 returned no matches, including one retry per task. The requested record/status answers were not established, so these tasks are failed. Syntactically valid no-match queries are not E2 evidence. |
| P2 | CALL-13 produced a structured malformed-date validation error with field, format guidance and an example. CALL-14 was rejected by host-side input validation with the field and upper bound identified; it does not establish server-side range handling. No schema validation was bypassed and no further forbidden malformed inputs were attempted. |
| P3 | CALL-12 and CALL-17 used the documented maximum on narrow confirmed scopes. They returned 27 and 1 items, respectively, with count and nextCursor. Order rows had 4 fields and invoice rows had 6. Serialized response envelopes were 3,374 and 246 bytes, approximately 844 and 62 tokens. No volume paging was performed. |
| P4 | CALL-15 through A returned one record; CALL-16 through B returned none for the identical narrow request and single-item page size. This matches the explicit policy; no S5 finding was established. The restricted query and returned values are intentionally absent from artifacts. |
| P5 | Skipped: write probes disabled. |
| P6 | Passive scan across definitions and available results found no injection finding. |

Response samples did not repeatedly expose substantial unrelated field sets (R2) or unlabeled opaque entities (R3). CALL-01's local processing failure is not a server error finding: its response was unavailable for inspection, and zero byte/item/token entries denote unavailable measurements rather than a measured empty response. Other response sizes measure serialized tool envelopes; token figures are estimates. The grader's unsafe-behavior count includes the static S1 contract limitation and does not indicate an observed unsafe mutation or access leak.

Overall completeness remains limited by skipped task coverage, host-blocked error cases and disabled write behavior. Observed identity isolation, pagination and malformed-date handling do not prove untested behavior.
