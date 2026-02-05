import { describe, it, expect, beforeEach, afterEach } from "vitest";
import nock from "nock";

const setEnv = () => {
  process.env.MCP_API_KEY = "test";
  process.env.TOURVISOR_SESSION = "session-token";
  process.env.TOURVISOR_REFERRER = "https://eto.travel/search/";
  process.env.TOURVISOR_SEARCH_HOST = "https://tourvisor.ru";
  process.env.TOURVISOR_RESULT_HOST = "https://search3.tourvisor.ru";
  process.env.TOURVISOR_POLL_INTERVAL_MS = "1";
  process.env.TOURVISOR_POLL_TIMEOUT_MS = "100";
  process.env.TOURVISOR_MAX_BLOCKS = "50";
  process.env.TOURVISOR_MAX_OFFERS = "300";
};

describe("polling", () => {
  beforeEach(() => {
    setEnv();
    nock.disableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
    nock.enableNetConnect();
  });

  it("collects offers and respects finished flag", async () => {
    const { searchTours } = await import("../src/tourvisor/polling");

    nock("https://tourvisor.ru")
      .get("/xml/modsearch.php")
      .query(true)
      .reply(200, {
        result: {
          requestid: 101,
          currency: "RUB",
          linkparam: 1,
          links: { hotellink: "https://tourcart.ru/hotel" }
        }
      });

    nock("https://search3.tourvisor.ru")
      .get("/modresult.php")
      .query(true)
      .reply(200, {
        data: {
          block: [
            {
              id: 1,
              operator: 9,
              hotel: [
                {
                  id: 77,
                  price: 120000,
                  tour: [
                    {
                      id: "tv123",
                      pr: 119000,
                      dt: "2024-06-01",
                      nt: 7,
                      op: 9,
                      reg: 44,
                      ct: 47,
                      ml: 3,
                      rm: 2
                    }
                  ]
                }
              ]
            }
          ],
          status: { progress: 50, finished: 0, requestid: 101 }
        }
      })
      .get("/modresult.php")
      .query(true)
      .reply(200, {
        data: {
          block: [],
          status: { progress: 100, finished: 1, requestid: 101 }
        }
      });

    const result = await searchTours({
      datefrom: "01.06.2024",
      dateto: "15.06.2024",
      nightsfrom: 6,
      nightsto: 14,
      adults: 2,
      country: 47,
      departure: 1,
      limit: 10
    });

    expect(result.offers).toHaveLength(1);
    expect(result.meta.requestid).toBe(101);
    expect(result.meta.finished).toBe(1);
    expect(result.meta.progress).toBe(100);
    expect(result.warnings).toEqual([]);
  });
});
