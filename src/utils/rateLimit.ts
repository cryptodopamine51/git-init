import { FastifyReply, FastifyRequest } from "fastify";
import { env } from "../config/env";

type RateLimitEntry = {
  count: number;
  resetAt: number;
};

const store = new Map<string, RateLimitEntry>();

const now = () => Date.now();

const getKey = (request: FastifyRequest) => request.ip;

const cleanupExpired = () => {
  const current = now();
  for (const [key, entry] of store.entries()) {
    if (entry.resetAt <= current) {
      store.delete(key);
    }
  }
};

export const rateLimitGuard = async (request: FastifyRequest, reply: FastifyReply) => {
  cleanupExpired();
  const key = getKey(request);
  const current = now();
  const windowMs = env.RATE_LIMIT_WINDOW_MS;
  const max = env.RATE_LIMIT_MAX;

  const entry = store.get(key);
  if (!entry || entry.resetAt <= current) {
    store.set(key, { count: 1, resetAt: current + windowMs });
    return;
  }

  if (entry.count >= max) {
    const retryAfterSeconds = Math.max(1, Math.ceil((entry.resetAt - current) / 1000));
    reply.header("Retry-After", String(retryAfterSeconds));
    return reply.status(429).send({ error: "Rate limit exceeded" });
  }

  entry.count += 1;
  store.set(key, entry);
};
