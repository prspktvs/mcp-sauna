import test from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { createReferenceServer } from "../reference-servers/server-core.mjs";

async function connected(variant, identity = "A", allowWrites = false) {
  const server = createReferenceServer({ variant, identity, allowWrites });
  const client = new Client({ name: "mcp-sauna-fixture-test", version: "0.1.0" });
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await Promise.all([server.connect(serverTransport), client.connect(clientTransport)]);
  return { server, client };
}

test("naive reference exposes seeded static design problems and bounded task targets", async () => {
  const { client, server } = await connected("naive");
  try {
    const tools = await client.listTools();
    assert.equal(tools.tools.length, 20);
    assert.ok(Math.ceil(Buffer.byteLength(JSON.stringify(tools.tools)) / 4) > 5000);
    assert.ok(tools.tools.some((tool) => tool.name === "get_or_update_stock"));
    assert.ok(tools.tools.some((tool) => tool.name === "delete_customer"));
    assert.equal(tools.tools.find((tool) => tool.name === "create_order")?.annotations, undefined);
    const result = await client.callTool({ name: "get_customer", arguments: { customerId: "CUS-100" } });
    assert.ok(Object.hasOwn(JSON.parse(result.content[0].text), "admin_note"));
    const missingId = await client.callTool({ name: "get_order_by_id", arguments: { orderId: "" } });
    assert.match(missingId.content[0].text, /"orders":\[\]/);
    const malformedDate = await client.callTool({ name: "list_orders", arguments: { fromDate: "tomorrow" } });
    assert.match(malformedDate.content[0].text, /"status":500/);
    assert.match(malformedDate.content[0].text, /"stack"/);
    const deleteResult = await client.callTool({ name: "delete_customer", arguments: { customerId: "CUS-100" } });
    assert.equal(deleteResult.isError, true);
  } finally {
    await client.close();
    await server.close();
  }
});

test("good reference paginates, documents annotations, and isolates test identities", async () => {
  const a = await connected("good", "A");
  const b = await connected("good", "B");
  try {
    const tools = await a.client.listTools();
    assert.ok(Math.ceil(Buffer.byteLength(JSON.stringify(tools.tools)) / 4) < 5000);
    const search = tools.tools.find((tool) => tool.name === "search_orders");
    assert.equal(search.annotations.readOnlyHint, true);
    const firstPage = await a.client.callTool({ name: "search_orders", arguments: { limit: 2 } });
    assert.match(firstPage.content[0].text, /"nextCursor":"2"/);
    const aInvoices = await a.client.callTool({ name: "search_invoices", arguments: { query: "Kelo" } });
    const bInvoices = await b.client.callTool({ name: "search_invoices", arguments: { query: "Kelo" } });
    assert.match(aInvoices.content[0].text, /INV-2026-501/);
    assert.match(bInvoices.content[0].text, /"count":0/);
    assert.equal(tools.tools.some((tool) => ["delete_customer", "cancel_order", "send_invoice"].includes(tool.name)), false);
  } finally {
    await Promise.all([a.client.close(), b.client.close(), a.server.close(), b.server.close()]);
  }
});

test("good reference enforces preview confirmation and idempotency", async () => {
  const { client, server } = await connected("good", "A", true);
  try {
    const preview = await client.callTool({ name: "preview_order", arguments: { customer: "Kelo Hotels Oy", sku: "HARJU-80", quantity: 2 } });
    const previewResult = JSON.parse(preview.content[0].text);
    const args = { previewId: previewResult.previewId, idempotencyKey: "sauna-test-key-01", confirmation: "CONFIRM" };
    const first = await client.callTool({ name: "place_order", arguments: args });
    const second = await client.callTool({ name: "place_order", arguments: args });
    assert.equal(JSON.parse(first.content[0].text).orderNumber, JSON.parse(second.content[0].text).orderNumber);
  } finally {
    await client.close();
    await server.close();
  }
});

test("reference writes are disabled unless explicitly enabled", async () => {
  const { client, server } = await connected("good");
  try {
    const result = await client.callTool({ name: "place_order", arguments: { previewId: "PREVIEW-invalid", idempotencyKey: "sauna-test-key-02", confirmation: "CONFIRM" } });
    assert.equal(result.isError, true);
    assert.match(result.content[0].text, /writes_disabled/);
  } finally {
    await client.close();
    await server.close();
  }
});

test("published stdio entrypoint starts as an MCP server", async () => {
  const serverPath = fileURLToPath(new URL("../reference-servers/server.mjs", import.meta.url));
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [serverPath],
    env: { ...process.env, SAUNA_VARIANT: "good", SAUNA_IDENTITY: "A" },
  });
  const client = new Client({ name: "mcp-sauna-stdio-test", version: "0.1.0" });
  try {
    await client.connect(transport);
    const listed = await client.listTools();
    assert.equal(listed.tools.length, 6);
  } finally {
    await client.close();
  }
});
