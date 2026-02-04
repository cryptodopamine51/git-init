import { FastifyInstance, FastifyReply, FastifyRequest } from "fastify";
import { getToolHandlers } from "./tools";
import { requireApiKey } from "./auth";

export const registerMcpRoutes = async (app: FastifyInstance) => {
  app.get("/health", async () => ({ ok: true }));

  app.get(
    "/mcp/sse",
    { preHandler: requireApiKey, config: { rateLimit: true } },
    async (request, reply) => {
      reply.raw.setHeader("Content-Type", "text/event-stream");
      reply.raw.setHeader("Cache-Control", "no-cache");
      reply.raw.setHeader("Connection", "keep-alive");
      reply.raw.flushHeaders?.();

      reply.raw.write(`event: ready\n`);
      reply.raw.write(`data: ${JSON.stringify({ ok: true })}\n\n`);

      request.raw.on("close", () => {
        reply.raw.end();
      });
    }
  );

  app.post(
    "/mcp/call",
    { preHandler: requireApiKey, config: { rateLimit: true } },
    async (request: FastifyRequest, reply: FastifyReply) => {
      const body = request.body as { tool?: string; args?: unknown };
      const toolName = body?.tool;
      if (!toolName) {
        return reply.status(400).send({ error: "Tool name is required" });
      }

      const handlers = getToolHandlers();
      const handler = handlers[toolName as keyof typeof handlers];
      if (!handler) {
        return reply.status(404).send({ error: "Tool not found" });
      }

      const result = await handler(body.args ?? {});
      return reply.send({ ok: true, tool: toolName, result });
    }
  );
};
