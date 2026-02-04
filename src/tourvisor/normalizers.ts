export type TourOffer = {
  offer_id: string;
  tour_id: string;
  price: number | "UNKNOWN";
  currency: string | "UNKNOWN";
  start_date: string | "UNKNOWN";
  nights: number | "UNKNOWN";
  hotel_id: number | "UNKNOWN";
  operator_id: number | "UNKNOWN";
  region_id: number | "UNKNOWN";
  country_id: number | "UNKNOWN";
  departure_id: number | "UNKNOWN";
  meal_id: number | "UNKNOWN";
  meal2_id: number | "UNKNOWN";
  room_id: number | "UNKNOWN";
  deep_link: string;
  source_raw: Record<string, unknown>;
};

export type TourBlock = {
  id: number;
  operator?: number;
  hotel?: Array<{ id?: number; price?: number; tour?: Array<Record<string, unknown>> }>;
};

export type NormalizeContext = {
  currency?: string;
  defaultCountry?: number;
  defaultDeparture?: number;
};

const resolveNumber = (value: unknown): number | "UNKNOWN" => {
  if (typeof value === "number") {
    return value;
  }
  if (typeof value === "string" && value.trim() !== "" && !Number.isNaN(Number(value))) {
    return Number(value);
  }
  return "UNKNOWN";
};

const resolveString = (value: unknown): string | "UNKNOWN" => {
  if (typeof value === "string" && value.trim() !== "") {
    return value;
  }
  return "UNKNOWN";
};

export const normalizeOffers = (block: TourBlock, context: NormalizeContext): TourOffer[] => {
  const offers: TourOffer[] = [];
  for (const hotel of block.hotel ?? []) {
    for (const tour of hotel.tour ?? []) {
      const tourId = resolveString((tour as { id?: unknown }).id);
      const priceValue = resolveNumber((tour as { pr?: unknown }).pr);
      const hotelPrice = resolveNumber(hotel.price);
      const normalizedPrice = priceValue !== "UNKNOWN" ? priceValue : hotelPrice;
      const startDate = resolveString((tour as { dt?: unknown }).dt);
      const nights = resolveNumber((tour as { nt?: unknown }).nt);
      const operatorId = resolveNumber((tour as { op?: unknown }).op ?? block.operator);
      const regionId = resolveNumber((tour as { reg?: unknown }).reg);
      const countryId = resolveNumber((tour as { ct?: unknown }).ct ?? context.defaultCountry);
      const departureId = resolveNumber(context.defaultDeparture);
      const mealId = resolveNumber((tour as { ml?: unknown }).ml ?? (tour as { mf?: unknown }).mf);
      const meal2Id = resolveNumber((tour as { mf?: unknown }).mf);
      const roomId = resolveNumber((tour as { rm?: unknown }).rm);

      const deepLink = tourId !== "UNKNOWN" ? `https://eto.travel/search/#tvtourid=${tourId}` : "UNKNOWN";

      offers.push({
        offer_id: tourId !== "UNKNOWN" ? tourId : "UNKNOWN",
        tour_id: tourId !== "UNKNOWN" ? tourId : "UNKNOWN",
        price: normalizedPrice,
        currency: context.currency ?? "UNKNOWN",
        start_date: startDate,
        nights,
        hotel_id: resolveNumber(hotel.id),
        operator_id: operatorId,
        region_id: regionId,
        country_id: countryId,
        departure_id: departureId,
        meal_id: mealId,
        meal2_id: meal2Id,
        room_id: roomId,
        deep_link: deepLink,
        source_raw: {
          block,
          hotel,
          tour
        }
      });
    }
  }
  return offers;
};
