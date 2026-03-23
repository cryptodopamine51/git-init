# Malakhov AI Digest — Slice 1 (Bot Foundation)

Первый вертикальный срез Telegram-бота с FastAPI backend, PostgreSQL, миграциями и базовой bot UX-логикой.

## Что реализовано в Slice 1
- FastAPI backend с `/health` и `/health/db`.
- SQLAlchemy 2.x + Alembic миграции.
- Таблицы `users` и `deliveries`.
- Telegram bot foundation на aiogram 3 (polling mode).
- `/start` onboarding с выбором режима подписки (`daily`/`weekly`).
- Экран «О боте».
- Раздел «Настройки» со сменой режима.
- Базовое меню: «Сегодня», «Итоги недели», «Настройки», «О боте».
- Заглушки для «Сегодня» и «Итоги недели».
- Логирование действий доставки в `deliveries`.
- Базовый каркас `jobs/` под APScheduler.

## Структура

```text
app/
  api/main.py
  bot/
    dispatcher.py
    handlers/common.py
    keyboards/reply.py
    texts.py
  core/
    config.py
    logging.py
  db/
    base.py
    session.py
    models/
      user.py
      delivery.py
  jobs/scheduler.py
  services/
    user_service.py
    delivery_service.py
    about_service.py
alembic/
  env.py
  versions/20260323_0001_slice1_foundation.py
tests/
  test_api_health.py
  test_services.py
scripts/run_bot.py
```

## Предварительные требования
- Python 3.12+
- Docker + Docker Compose

## Локальный запуск

1. Скопировать env:
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

5. Запустить API:
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

6. Запустить бота (в отдельном терминале):
```bash
python scripts/run_bot.py
```

## Проверка
- API health:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/db
```

## Тесты
```bash
pytest -q
```

## Scope Slice 1 (осознанные ограничения)
Не реализованы ingestion, events, scoring, digest-builder, knowledge base, webhook deployment, admin и web UI.
