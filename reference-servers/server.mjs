import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createReferenceServer } from "./server-core.mjs";

const variant = process.env.SAUNA_VARIANT ?? "good";
const identity = process.env.SAUNA_IDENTITY ?? "A";
const server = createReferenceServer({ variant, identity });
await server.connect(new StdioServerTransport());
