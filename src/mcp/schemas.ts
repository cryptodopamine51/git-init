import { z } from "zod";

export const getDictionariesSchema = z.object({
  type: z.string(),
  hotcountry: z.number().nullable().optional(),
  flycountry: z.number().nullable().optional(),
  flydeparture: z.number().nullable().optional(),
  cndep: z.number().nullable().optional(),
  formmode: z.number().nullable().optional(),
  format: z.literal("json").default("json")
});

export const searchToursSchema = z.object({
  datefrom: z.string(),
  dateto: z.string(),
  regular: z.number().optional(),
  nightsfrom: z.number(),
  nightsto: z.number(),
  adults: z.number(),
  child: z.number().optional(),
  meal: z.number().optional(),
  rating: z.number().optional(),
  country: z.number(),
  departure: z.number(),
  pricefrom: z.number().optional(),
  priceto: z.number().optional(),
  currency: z.number().optional(),
  actype: z.number().optional(),
  formmode: z.number().optional(),
  pricetype: z.number().optional(),
  limit: z.number().optional()
});

export const tourDetailsSchema = z.object({
  tourid: z.string(),
  currency: z.number().optional().default(0)
});

export type GetDictionariesInput = z.infer<typeof getDictionariesSchema>;
export type SearchToursInput = z.infer<typeof searchToursSchema>;
export type TourDetailsInput = z.infer<typeof tourDetailsSchema>;
