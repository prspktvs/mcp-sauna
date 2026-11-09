import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createReferenceServer } from "./server-core.mjs";

const variant = process.env.SAUNA_VARIANT ?? "good";
const identity = process.env.SAUNA_IDENTITY ?? "A";
const allowWrites = process.env.SAUNA_ALLOW_WRITES === "1";
const server = createReferenceServer({ variant, identity, allowWrites });
await server.connect(new StdioServerTransport());
