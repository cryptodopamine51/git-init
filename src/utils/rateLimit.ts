import { FastifyInstance } from "fastify";
import rateLimit from "@fastify/rate-limit";
import { env } from "../config/env";

export const registerRateLimit = async (app: FastifyInstance) => {
  await app.register(rateLimit, {
    max: env.RATE_LIMIT_MAX,
    timeWindow: env.RATE_LIMIT_WINDOW_MS,
    keyGenerator: (request) => request.ip,
    global: false
  });
};
