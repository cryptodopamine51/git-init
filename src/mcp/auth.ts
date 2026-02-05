import { FastifyRequest, FastifyReply } from "fastify";
import { env } from "../config/env";

export const requireApiKey = async (request: FastifyRequest, reply: FastifyReply) => {
  const apiKey = request.headers["x-api-key"];
  if (!apiKey || apiKey !== env.MCP_API_KEY) {
    return reply.status(401).send({ error: "Unauthorized" });
  }
};
