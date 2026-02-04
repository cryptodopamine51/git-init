import { endpoints } from "./endpoints";
import { fetchJson } from "./client";
import { env } from "../config/env";

export type ListDevResponse = Record<string, unknown>;

export type DictionaryParams = {
  type: string;
  hotcountry?: number | null;
  flycountry?: number | null;
  flydeparture?: number | null;
  cndep?: number | null;
  formmode?: number | null;
  format?: "json";
};

export const getDictionaries = async (params: DictionaryParams) => {
  const url = new URL(endpoints.listdev.toString());
  return fetchJson<ListDevResponse>(url, {
    type: params.type,
    hotcountry: params.hotcountry ?? undefined,
    flycountry: params.flycountry ?? undefined,
    flydeparture: params.flydeparture ?? undefined,
    cndep: params.cndep ?? undefined,
    formmode: params.formmode ?? undefined,
    format: params.format ?? "json",
    referrer: env.TOURVISOR_REFERRER,
    session: env.TOURVISOR_SESSION
  });
};
