import { env } from "../config/env";
import { getDictionariesSchema, searchToursSchema, tourDetailsSchema } from "./schemas";
import { getDictionaries } from "../tourvisor/dictionaries";
import { searchTours } from "../tourvisor/polling";
import { fetchJson } from "../tourvisor/client";
import { endpoints } from "../tourvisor/endpoints";

export type ToolResponse = {
  data?: unknown;
  offers?: unknown;
  meta: Record<string, unknown>;
  warnings: string[];
};

export const toolHandlers = {
  get_dictionaries: async (input: unknown): Promise<ToolResponse> => {
    const parsed = getDictionariesSchema.parse(input);
    const data = await getDictionaries(parsed);
    return {
      data,
      meta: { source: "tourvisor:listdev", session_used: true },
      warnings: []
    };
  },
  search_tours: async (input: unknown): Promise<ToolResponse> => {
    const parsed = searchToursSchema.parse(input);
    const result = await searchTours(parsed);
    return {
      offers: result.offers,
      meta: result.meta,
      warnings: result.warnings
    };
  }
};

export const optionalTools = {
  get_tour_details: async (input: unknown): Promise<ToolResponse> => {
    const parsed = tourDetailsSchema.parse(input);
    const url = new URL(endpoints.modact.toString());
    const data = await fetchJson(url, {
      currency: parsed.currency ?? 0,
      tourid: parsed.tourid,
      referrer: env.TOURVISOR_REFERRER,
      session: env.TOURVISOR_USE_SESSION_FOR_MODACT ? env.TOURVISOR_SESSION : undefined
    });
    return {
      data,
      meta: { source: "tourvisor:modact", session_used: env.TOURVISOR_USE_SESSION_FOR_MODACT },
      warnings: []
    };
  }
};

export const getToolHandlers = () => {
  if (env.ENABLE_TOUR_DETAILS) {
    return { ...toolHandlers, ...optionalTools };
  }
  return toolHandlers;
};
