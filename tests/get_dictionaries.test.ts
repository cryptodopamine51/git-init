import { describe, it, expect, beforeEach, afterEach } from "vitest";
import nock from "nock";

const setEnv = () => {
  process.env.MCP_API_KEY = "test";
  process.env.TOURVISOR_SESSION = "session-token";
  process.env.TOURVISOR_REFERRER = "https://eto.travel/search/";
  process.env.TOURVISOR_SEARCH_HOST = "https://tourvisor.ru";
  process.env.TOURVISOR_RESULT_HOST = "https://search3.tourvisor.ru";
};

describe("get_dictionaries", () => {
  beforeEach(() => {
    setEnv();
    nock.disableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
    nock.enableNetConnect();
  });

  it("fetches listdev dictionaries", async () => {
    const { getDictionaries } = await import("../src/tourvisor/dictionaries");

    nock("https://tourvisor.ru")
      .get("/xml/listdev.php")
      .query(true)
      .reply(200, {
        lists: {
          departures: {
            departure: [{ id: 1, name: "Москва" }]
          }
        }
      });

    const result = await getDictionaries({ type: "departure" });
    expect(result).toHaveProperty("lists");
  });
});
