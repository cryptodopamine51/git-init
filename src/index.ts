import fastify from "fastify";
import { registerMcpRoutes } from "./mcp/server";
import { env } from "./config/env";

const app = fastify({
  logger: {
    level: "info"
  }
});

const start = async () => {
await registerMcpRoutes(app);

await app.ready();
app.log.info("\n" + app.printRoutes());

  await app.listen({ port: env.PORT, host: "0.0.0.0" });
};

start().catch((error) => {
  app.log.error({ error }, "Failed to start server");
  process.exit(1);
});
