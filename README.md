# Malakhov AI Digest — Slices 1-3

## Что уже покрыто
- Slice 1: backend + Telegram foundation.
- Slice 2: ingestion (`sources`, `raw_items`, `source_runs`).
- Slice 3: normalization + event clustering + classification + scoring + events preview.

## Slice 3: ключевые возможности
- Таблицы `events`, `event_sources`, `event_categories`, `event_tags`.
- Pipeline `fetched -> normalized -> clustered | discarded`.
- Rule-based normalization (clean text, entities, outbound links, language).
- Deterministic clustering (canonical URL + title/entity signature).
- Rule-based classification по секциям:
  - `important`, `ai_news`, `coding`, `investments`, `alpha`.
- Configurable scoring:
  - `importance_score`, `market_impact_score`, `ai_news_score`, `coding_score`, `investment_score`, `confidence_score`.
- Выбор primary source + supporting sources.
- Internal preview events endpoints.

## Локальный запуск

```bash
cp .env.example .env
docker compose up -d
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
alembic upgrade head
python scripts/seed_sources.py
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Запуск ingestion и process-events вручную

```bash
curl -X POST http://localhost:8000/internal/jobs/ingest
curl -X POST http://localhost:8000/internal/jobs/process-events
```

## Internal preview

```bash
curl http://localhost:8000/internal/sources
curl http://localhost:8000/internal/raw-items?limit=20
curl http://localhost:8000/internal/source-runs?limit=20
curl http://localhost:8000/internal/events?limit=20
curl http://localhost:8000/internal/events/1
curl http://localhost:8000/internal/events/preview/day/2026-03-23
```

## Как проверить clustering/classification локально
1. Засейдить источники и прогнать ingestion.
2. Прогнать `process-events`.
3. Проверить `/internal/events` и `/internal/events/{id}`.
4. Проверить primary section в `event_categories` и score-поля в `events`.

## Тесты

```bash
pytest -q tests/test_services.py tests/test_api_health.py tests/test_ingestion.py tests/test_events_pipeline.py
```

## Ограничения Slice 3
- Нет digest builder/daily/weekly выпуска и delivery контента.
- Нет advanced ML ranking и UI-редактуры.
- `alpha` присутствует как section type/placeholder, но не формируется отдельным источником автоматически.
