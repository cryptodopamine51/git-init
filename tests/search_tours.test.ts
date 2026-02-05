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
};

describe("search_tours tool", () => {
  beforeEach(() => {
    setEnv();
    nock.disableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
    nock.enableNetConnect();
  });

  it("returns offers with meta", async () => {
    const { toolHandlers } = await import("../src/mcp/tools");

    nock("https://tourvisor.ru")
      .get("/xml/modsearch.php")
      .query(true)
      .reply(200, {
        result: {
          requestid: 202,
          currency: "RUB"
        }
      });

    nock("https://search3.tourvisor.ru")
      .get("/modresult.php")
      .query(true)
      .reply(200, {
        data: {
          block: [
            {
              id: 3,
              operator: 2,
              hotel: [
                {
                  id: 10,
                  price: 90000,
                  tour: [
                    {
                      id: "tv999",
                      pr: 88000,
                      dt: "2024-07-01",
                      nt: 10,
                      op: 2,
                      reg: 11,
                      ct: 47
                    }
                  ]
                }
              ]
            }
          ],
          status: { progress: 100, finished: 1, requestid: 202 }
        }
      });

    const response = await toolHandlers.search_tours({
      datefrom: "01.07.2024",
      dateto: "15.07.2024",
      nightsfrom: 7,
      nightsto: 14,
      adults: 2,
      country: 47,
      departure: 1,
      limit: 5
    });

    expect(response.offers).toHaveLength(1);
    expect(response.meta).toHaveProperty("requestid", 202);
  });
});
