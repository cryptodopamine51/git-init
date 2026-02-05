import { endpoints } from "./endpoints";
import { fetchJson } from "./client";
import { env } from "../config/env";
import { normalizeOffers, TourOffer, TourBlock } from "./normalizers";
import { sleep } from "../utils/sleep";

export type SearchParams = {
  datefrom: string;
  dateto: string;
  regular?: number;
  nightsfrom: number;
  nightsto: number;
  adults: number;
  child?: number;
  meal?: number;
  rating?: number;
  country: number;
  departure: number;
  pricefrom?: number;
  priceto?: number;
  currency?: number;
  actype?: number;
  formmode?: number;
  pricetype?: number;
  limit?: number;
};

export type ModSearchResponse = {
  result?: {
    requestid?: number;
    currency?: string;
    linkparam?: number;
    links?: Record<string, string>;
    searchident?: string;
  };
};

export type ModResultResponse = {
  data?: {
    block?: TourBlock[];
    status?: {
      progress?: number;
      finished?: number;
      requestid?: number;
    };
  };
  debug?: Record<string, unknown>;
};

export type SearchResult = {
  offers: TourOffer[];
  meta: {
    requestid: number;
    finished: number | "UNKNOWN";
    progress: number | "UNKNOWN";
    blocks_seen: number;
    offers_total_collected: number;
  };
  warnings: string[];
};

const parseStatusValue = (value: unknown): number | "UNKNOWN" => {
  if (typeof value === "number") {
    return value;
  }
  if (typeof value === "string" && value.trim() !== "" && !Number.isNaN(Number(value))) {
    return Number(value);
  }
  return "UNKNOWN";
};

export const searchTours = async (params: SearchParams): Promise<SearchResult> => {
  const modsearchUrl = new URL(endpoints.modsearch.toString());
  const modsearchResponse = await fetchJson<ModSearchResponse>(modsearchUrl, {
    datefrom: params.datefrom,
    dateto: params.dateto,
    regular: params.regular ?? 1,
    nightsfrom: params.nightsfrom,
    nightsto: params.nightsto,
    adults: params.adults,
    child: params.child ?? 0,
    meal: params.meal ?? 0,
    rating: params.rating ?? 0,
    country: params.country,
    departure: params.departure,
    pricefrom: params.pricefrom ?? 0,
    priceto: params.priceto ?? 0,
    currency: params.currency ?? 0,
    actype: params.actype ?? 0,
    formmode: params.formmode ?? 0,
    pricetype: params.pricetype ?? 0,
    referrer: env.TOURVISOR_REFERRER,
    session: env.TOURVISOR_SESSION
  });

  const requestId = modsearchResponse.result?.requestid;
  const currency = modsearchResponse.result?.currency ?? "UNKNOWN";
  if (typeof requestId !== "number") {
    throw new Error("Tourvisor modsearch did not return requestid");
  }

  const warnings: string[] = [];
  const offersMap = new Map<string, TourOffer>();
  const seenBlockIds = new Set<number>();
  let lastblock: number | undefined;
  let progress: number | "UNKNOWN" = "UNKNOWN";
  let finished: number | "UNKNOWN" = "UNKNOWN";

  const startTime = Date.now();
  const timeoutMs = env.TOURVISOR_POLL_TIMEOUT_MS;
  const maxOffers = params.limit ?? env.TOURVISOR_MAX_OFFERS;

  while (Date.now() - startTime < timeoutMs) {
    const modresultUrl = new URL(endpoints.modresult.toString());
    const modresultResponse = await fetchJson<ModResultResponse>(modresultUrl, {
      requestid: requestId,
      lastblock,
      referrer: env.TOURVISOR_REFERRER,
      session: env.TOURVISOR_SESSION
    });

    const blocks = modresultResponse.data?.block ?? [];
    for (const block of blocks) {
      if (typeof block.id === "number" && !seenBlockIds.has(block.id)) {
        seenBlockIds.add(block.id);
        const normalized = normalizeOffers(block, {
          currency,
          defaultCountry: params.country,
          defaultDeparture: params.departure
        });
        for (const offer of normalized) {
          if (!offersMap.has(offer.offer_id)) {
            offersMap.set(offer.offer_id, offer);
          }
        }
      }
    }

    const blockIds = blocks.map((block) => block.id).filter((id): id is number => typeof id === "number");
    if (blockIds.length > 0) {
      lastblock = Math.max(lastblock ?? 0, ...blockIds);
    }

    const status = modresultResponse.data?.status;
    progress = parseStatusValue(status?.progress);
    finished = parseStatusValue(status?.finished);

    if ((typeof finished === "number" && finished === 1) || (typeof progress === "number" && progress >= 100)) {
      break;
    }

    if (offersMap.size >= maxOffers) {
      break;
    }

    if (seenBlockIds.size >= env.TOURVISOR_MAX_BLOCKS) {
      warnings.push("MAX_BLOCKS_REACHED");
      break;
    }

    await sleep(env.TOURVISOR_POLL_INTERVAL_MS);
  }

  if (Date.now() - startTime >= timeoutMs) {
    warnings.push("TIMEOUT_PARTIAL_RESULTS");
  }

  const offers = Array.from(offersMap.values()).slice(0, maxOffers);

  return {
    offers,
    meta: {
      requestid: requestId,
      finished,
      progress,
      blocks_seen: seenBlockIds.size,
      offers_total_collected: offers.length
    },
    warnings
  };
};
