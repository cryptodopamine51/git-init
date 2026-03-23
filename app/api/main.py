from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import internal_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import check_db_connection
from app.jobs.ingest_job import register_ingestion_job
from app.jobs.process_events_job import register_process_events_job
from app.jobs.scheduler import create_scheduler


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    scheduler = create_scheduler()
    register_ingestion_job(scheduler)
    register_process_events_job(scheduler)
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)


settings = get_settings()
app = FastAPI(title="Malakhov AI Digest API", lifespan=lifespan)
app.include_router(internal_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "malakhov-ai-digest",
        "environment": settings.app_env,
    }


@app.get("/health/db")
async def health_db() -> dict[str, str]:
    is_connected = await check_db_connection()
    return {
        "status": "ok" if is_connected else "error",
        "service": "malakhov-ai-digest",
        "environment": settings.app_env,
    }
