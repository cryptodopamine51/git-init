import { request } from "undici";
import { HttpError } from "../utils/errors";

export const fetchJson = async <T>(url: URL, params: Record<string, string | number | undefined>) => {
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      url.searchParams.set(key, String(value));
    }
  });

  const { statusCode, body } = await request(url.toString(), {
    method: "GET",
    headers: {
      Accept: "application/json"
    }
  });

  const text = await body.text();
  if (statusCode < 200 || statusCode >= 300) {
    throw new HttpError(statusCode, "Tourvisor request failed", { url: url.toString(), body: text });
  }

  try {
    return JSON.parse(text) as T;
  } catch (error) {
    throw new HttpError(502, "Invalid JSON from Tourvisor", { url: url.toString(), error, text });
  }
};
