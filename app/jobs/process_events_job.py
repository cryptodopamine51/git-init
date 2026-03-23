import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.session import SessionLocal
from app.services.events.process_events import ProcessEventsService

logger = logging.getLogger(__name__)


async def run_process_events_job() -> None:
    async with SessionLocal() as session:
        result = await ProcessEventsService(session).process()
    logger.info(
        "Process events job done: normalized=%s clustered=%s discarded=%s created=%s updated=%s",
        result.normalized_count,
        result.clustered_count,
        result.discarded_count,
        result.events_created,
        result.events_updated,
    )


def register_process_events_job(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        run_process_events_job,
        trigger="interval",
        minutes=20,
        id="process_events_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
