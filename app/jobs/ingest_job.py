import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.session import SessionLocal
from app.services.ingestion.ingestion_service import IngestionService

logger = logging.getLogger(__name__)


async def run_ingestion_job() -> None:
    async with SessionLocal() as session:
        service = IngestionService(session)
        runs = await service.run_all_active_sources()
        logger.info("Ingestion job completed for %s sources", len(runs))


def register_ingestion_job(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        run_ingestion_job,
        trigger="interval",
        minutes=30,
        id="ingestion_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
