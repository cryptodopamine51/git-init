# Malakhov AI Digest — Slices 1-2

Проект включает:
- Slice 1: foundation backend + Telegram bot;
- Slice 2: source ingestion + `raw_items` storage.

## Реализовано (Slice 2)
- Таблицы `sources`, `raw_items`, `source_runs`.
- Адаптерный ingestion contract.
- 2 адаптера:
  - RSS/Atom adapter;
  - JSON feed adapter (как простой website feed).
- Ingestion service c dedup по `(source_id, external_id)`.
- Source run logging (`success` / `failed`).
- APScheduler job для периодического ingestion.
- Internal preview endpoints:
  - `GET /internal/sources`
  - `GET /internal/raw-items`
  - `GET /internal/source-runs`
  - `POST /internal/jobs/ingest`
- Seed scripts для стартовых источников.

## Локальный запуск

1. Создать `.env`:
```bash
cp .env.example .env
```

2. Поднять PostgreSQL:
```bash
docker compose up -d
```

3. Установить зависимости:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

4. Применить миграции:
```bash
alembic upgrade head
```

5. Засеять источники:
```bash
python scripts/seed_sources.py
```

6. Запустить API:
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

7. (Опционально) запустить Telegram polling bot:
```bash
python scripts/run_bot.py
```

## Ручной запуск ingestion

Через internal endpoint:
```bash
curl -X POST http://localhost:8000/internal/jobs/ingest
```

Проверка источников и raw-items:
```bash
curl http://localhost:8000/internal/sources
curl http://localhost:8000/internal/raw-items?limit=20
curl http://localhost:8000/internal/source-runs?limit=20
```

## Поддерживаемые источники в Slice 2
- `rss_feed` (RSS/Atom URL)
- `official_blog` (RSS/Atom URL)
- `website` (JSON feed endpoint формата `{ "items": [...] }`)

## Тесты
```bash
pytest -q tests/test_services.py tests/test_api_health.py tests/test_ingestion.py
```

## Ограничения Slice 2
Не входят в этот этап: normalization pipeline, clustering, scoring, digest builder, Telegram content delivery, ingestion из X/Twitter/сложных каналов.
