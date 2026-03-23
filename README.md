# Malakhov AI Digest

Backend платформа для Telegram-дайджеста по ИИ:
- ingestion источников,
- нормализация и кластеризация в события,
- классификация и scoring,
- foundation для daily/weekly delivery.

## Текущий статус

Реализованы foundation-слои:
- **Slice 1**: FastAPI + PostgreSQL + Alembic + Telegram bot foundation.
- **Slice 2**: sources/raw_items/source_runs + ingestion adapters + preview endpoints.
- **Slice 3**: normalization + clustering + classification + scoring + events preview.

Следующая цель: построить **рабочий daily/weekly delivery layer** поверх event-layer.

## Архитектура (высокоуровнево)

- `app/api/` — API и internal preview routes.
- `app/db/` — SQLAlchemy модели и session layer.
- `app/services/ingestion/` — сбор источников в `raw_items`.
- `app/services/normalization/` — очистка и обогащение raw items.
- `app/services/clustering/` — группировка материалов в events.
- `app/services/classification/` — section assignment.
- `app/services/scoring/` — rule-based scores.
- `app/services/events/` — orchestration pipeline process-events.
- `app/jobs/` — APScheduler jobs (`ingest`, `process-events`).
- `scripts/` — утилиты локального запуска и seed.

## Секреты и переменные окружения

Секреты **не хранятся в репозитории**.

Используйте только environment variables:
- `BOT_TOKEN`
- `DATABASE_URL`

Пример локального `.env` можно сделать на базе `.env.example`, но реальные значения подставляются из окружения.

## Быстрый локальный старт

```bash
cp .env.example .env
# заполните .env без коммита секретов

docker compose up -d
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
alembic upgrade head
python scripts/seed_sources.py
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Полезные internal endpoints

```bash
# health
curl http://localhost:8000/health
curl http://localhost:8000/health/db

# ingestion
curl -X POST http://localhost:8000/internal/jobs/ingest
curl http://localhost:8000/internal/sources
curl http://localhost:8000/internal/raw-items?limit=20
curl http://localhost:8000/internal/source-runs?limit=20

# events pipeline
curl -X POST http://localhost:8000/internal/jobs/process-events
curl http://localhost:8000/internal/events?limit=20
curl http://localhost:8000/internal/events/1
curl http://localhost:8000/internal/events/preview/day/2026-03-23
```

## Тесты

```bash
pytest -q tests/test_services.py tests/test_api_health.py tests/test_ingestion.py tests/test_events_pipeline.py
```

## Подготовка к следующей итерации (delivery layer)

Для следующего шага (daily/weekly delivery) README и проект должны опираться на:
- `AGENTS.md`
- `docs/editorial_rules.md`
- `data/seed_sources.csv`

> В текущем состоянии репозитория `docs/editorial_rules.md` и `data/seed_sources.csv` отсутствуют. Добавьте их в следующей итерации перед внедрением delivery-логики.

## Безопасность

- Не выводите значения `BOT_TOKEN`, `DATABASE_URL` в логах/ответах.
- Не коммитьте реальные секреты в `.env`, README и любые файлы репозитория.
