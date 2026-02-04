# MCP-сервер для поиска туров Tourvisor (eto.travel)

Готовый к запуску MVP MCP-сервера на Node.js + TypeScript, который подключает LLM и выполняет поиск туров через публичный поиск eto.travel, используя наблюдаемые HTTP endpoint’ы Tourvisor.

## Быстрый старт

```bash
npm install
cp .env.example .env
npm run dev
```

Проверка здоровья:

```bash
curl http://localhost:3000/health
```

## Пример .env

```env
PORT=3000
MCP_API_KEY=change_me
TOURVISOR_SESSION=your_session_token
TOURVISOR_REFERRER=https://eto.travel/search/
TOURVISOR_SEARCH_HOST=https://tourvisor.ru
TOURVISOR_RESULT_HOST=https://search3.tourvisor.ru
TOURVISOR_POLL_INTERVAL_MS=500
TOURVISOR_POLL_TIMEOUT_MS=45000
TOURVISOR_MAX_BLOCKS=50
TOURVISOR_MAX_OFFERS=300
ENABLE_TOUR_DETAILS=false
TOURVISOR_USE_SESSION_FOR_MODACT=true
RATE_LIMIT_MAX=60
RATE_LIMIT_WINDOW_MS=60000
```

## MCP endpoint’ы

Сервер реализует SSE-транспорт и требует заголовок `x-api-key` на MCP endpoint’ах:

- `GET /mcp/sse` — SSE-стрим (требует `x-api-key`)
- `POST /mcp/call` — вызов tool (требует `x-api-key`)

Формат вызова:

```json
{
  "tool": "search_tours",
  "args": { "...": "..." }
}
```

## Примеры вызова MCP tools (curl)

### search_tours

```bash
curl -X POST http://localhost:3000/mcp/call \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MCP_API_KEY" \
  -d '{
    "tool": "search_tours",
    "args": {
      "datefrom": "01.06.2024",
      "dateto": "15.06.2024",
      "regular": 1,
      "nightsfrom": 6,
      "nightsto": 14,
      "adults": 2,
      "child": 0,
      "meal": 0,
      "rating": 0,
      "country": 47,
      "departure": 1,
      "pricefrom": 0,
      "priceto": 0,
      "currency": 0,
      "actype": 0,
      "formmode": 0,
      "pricetype": 0,
      "limit": 50
    }
  }'
```

### get_dictionaries

```bash
curl -X POST http://localhost:3000/mcp/call \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MCP_API_KEY" \
  -d '{
    "tool": "get_dictionaries",
    "args": {
      "type": "departure,allcountry,country,region,subregions,operator",
      "formmode": 0,
      "format": "json"
    }
  }'
```

## Описание полей search_tours

Обязательные параметры:
- `datefrom` — дата начала (формат «DD.MM.YYYY»).
- `dateto` — дата окончания (формат «DD.MM.YYYY»).
- `nightsfrom` — минимальная длительность.
- `nightsto` — максимальная длительность.
- `adults` — количество взрослых.
- `country` — код страны.
- `departure` — код вылета.

Опциональные параметры:
- `regular`, `child`, `meal`, `rating`, `pricefrom`, `priceto`, `currency`, `actype`, `formmode`, `pricetype`.
- `limit` — ограничение количества офферов в ответе.

## Ограничения и особенности

- Поиск построен на «modsearch → polling modresult».
- Для корректных ответов требуется актуальный `TOURVISOR_SESSION`.
- Поллинг завершится по `finished==1`, `progress==100`, достижению лимитов или таймауту.
- Лимиты регулируются через `TOURVISOR_POLL_INTERVAL_MS`, `TOURVISOR_POLL_TIMEOUT_MS`, `TOURVISOR_MAX_BLOCKS`, `TOURVISOR_MAX_OFFERS`.
- Поле `deep_link` возвращается как «UNKNOWN», если отсутствует идентификатор тура.
- На MCP endpoint’ах включён rate limit по IP.
- `get_tour_details` выключен по умолчанию. Включается через `ENABLE_TOUR_DETAILS=true`.

## Деплой (Render / Railway)

1. Создайте новый сервис из репозитория.
2. Укажите переменные окружения из раздела «Пример .env».
3. Команда сборки: `npm install && npm run build`.
4. Команда запуска: `npm run start`.
5. Проверьте `/health` после деплоя.

## Структура проекта

```
/src
  /config
    env.ts
  /mcp
    server.ts
    tools.ts
    schemas.ts
    auth.ts
  /tourvisor
    client.ts
    endpoints.ts
    polling.ts
    normalizers.ts
    dictionaries.ts
  /utils
    sleep.ts
    errors.ts
    rateLimit.ts
  index.ts
/tests
  search_tours.test.ts
  get_dictionaries.test.ts
  polling.test.ts
Dockerfile
README.md
.env.example
package.json
tsconfig.json
```
