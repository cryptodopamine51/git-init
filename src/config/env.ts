import { z } from "zod";
import dotenv from "dotenv";

dotenv.config();

const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  MCP_API_KEY: z.string().min(1, "MCP_API_KEY is required"),
  TOURVISOR_SESSION: z.string().min(1, "TOURVISOR_SESSION is required"),
  TOURVISOR_REFERRER: z.string().url().default("https://eto.travel/search/"),
  TOURVISOR_SEARCH_HOST: z.string().url().default("https://tourvisor.ru"),
  TOURVISOR_RESULT_HOST: z.string().url().default("https://search3.tourvisor.ru"),
  TOURVISOR_POLL_INTERVAL_MS: z.coerce.number().default(500),
  TOURVISOR_POLL_TIMEOUT_MS: z.coerce.number().default(45000),
  TOURVISOR_MAX_BLOCKS: z.coerce.number().default(50),
  TOURVISOR_MAX_OFFERS: z.coerce.number().default(300),
  ENABLE_TOUR_DETAILS: z.coerce.boolean().default(false),
  TOURVISOR_USE_SESSION_FOR_MODACT: z.coerce.boolean().default(true),
  RATE_LIMIT_MAX: z.coerce.number().default(60),
  RATE_LIMIT_WINDOW_MS: z.coerce.number().default(60000)
});

export type EnvConfig = z.infer<typeof envSchema>;

export const env = envSchema.parse(process.env);
