import { env } from "../config/env";

export const endpoints = {
  modsearch: new URL("/xml/modsearch.php", env.TOURVISOR_SEARCH_HOST),
  modresult: new URL("/modresult.php", env.TOURVISOR_RESULT_HOST),
  listdev: new URL("/xml/listdev.php", env.TOURVISOR_SEARCH_HOST),
  modact: new URL("/xml/modact.php", env.TOURVISOR_SEARCH_HOST)
};
