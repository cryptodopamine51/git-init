from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event, EventCategory, EventSource, EventTag, RawItem, SourceRun
from app.db.session import get_async_session
from app.services.events.process_events import ProcessEventsService
from app.services.ingestion.ingestion_service import IngestionService
from app.services.sources.registry import SourceRegistryService

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/sources")
async def get_sources(session: AsyncSession = Depends(get_async_session)) -> list[dict]:
    sources = await SourceRegistryService(session).list_sources(active_only=False)
    return [
        {
            "id": source.id,
            "source_type": source.source_type.value,
            "title": source.title,
            "handle_or_url": source.handle_or_url,
            "priority_weight": source.priority_weight,
            "is_active": source.is_active,
            "meta_json": source.meta_json,
        }
        for source in sources
    ]


@router.get("/raw-items")
async def get_raw_items(
    source_id: int | None = None,
    limit: int = Query(default=20, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    query = select(RawItem).order_by(RawItem.fetched_at.desc()).limit(limit)
    if source_id:
        query = query.where(RawItem.source_id == source_id)
    result = await session.execute(query)
    items = result.scalars().all()
    return [
        {
            "id": item.id,
            "source_id": item.source_id,
            "external_id": item.external_id,
            "canonical_url": item.canonical_url,
            "raw_title": item.raw_title,
            "status": item.status.value,
            "published_at": item.published_at,
        }
        for item in items
    ]


@router.post("/jobs/ingest")
async def run_ingest(request: Request, session: AsyncSession = Depends(get_async_session)) -> dict:
    adapter_registry = getattr(request.app.state, "adapter_registry", None)
    runs = await IngestionService(session, adapter_registry=adapter_registry).run_all_active_sources()
    return {
        "status": "ok",
        "runs": [
            {
                "source_id": run.source_id,
                "run_id": run.id,
                "fetched_count": run.fetched_count,
                "inserted_count": run.inserted_count,
                "status": run.status.value,
                "error_message": run.error_message,
            }
            for run in runs
        ],
    }


@router.post("/jobs/process-events")
async def run_process_events(session: AsyncSession = Depends(get_async_session)) -> dict:
    result = await ProcessEventsService(session).process()
    return {
        "status": "ok",
        "normalized_count": result.normalized_count,
        "discarded_count": result.discarded_count,
        "clustered_count": result.clustered_count,
        "events_created": result.events_created,
        "events_updated": result.events_updated,
    }


@router.get("/source-runs")
async def get_source_runs(
    limit: int = Query(default=20, le=200),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    query = select(SourceRun).order_by(SourceRun.started_at.desc()).limit(limit)
    result = await session.execute(query)
    runs = result.scalars().all()
    return [
        {
            "id": run.id,
            "source_id": run.source_id,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
            "status": run.status.value,
            "fetched_count": run.fetched_count,
            "inserted_count": run.inserted_count,
            "error_message": run.error_message,
        }
        for run in runs
    ]


@router.get("/events")
async def get_events(
    section: str | None = None,
    date_value: date | None = Query(default=None, alias="date"),
    limit: int = Query(default=20, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    query = select(Event).order_by(Event.event_date.desc(), Event.importance_score.desc()).limit(limit)
    if date_value:
        query = query.where(Event.event_date == date_value)
    result = await session.execute(query)
    events = result.scalars().all()

    if section:
        events = [
            event
            for event in events
            if any(cat.section.value == section for cat in (await session.execute(select(EventCategory).where(EventCategory.event_id == event.id))).scalars().all())
        ]

    return [
        {
            "id": event.id,
            "event_date": event.event_date,
            "title": event.title,
            "importance_score": event.importance_score,
            "primary_source_id": event.primary_source_id,
            "primary_source_url": event.primary_source_url,
            "is_highlight": event.is_highlight,
        }
        for event in events
    ]


@router.get("/events/preview/day/{day}")
async def preview_day(day: date, session: AsyncSession = Depends(get_async_session)) -> dict:
    events = (await session.execute(select(Event).where(Event.event_date == day).order_by(Event.importance_score.desc()))).scalars().all()
    grouped: dict[str, list[dict]] = {}
    for event in events:
        categories = (await session.execute(select(EventCategory).where(EventCategory.event_id == event.id))).scalars().all()
        if not categories:
            grouped.setdefault("unclassified", []).append({"id": event.id, "title": event.title})
            continue
        primary = next((c.section.value for c in categories if c.is_primary_section), categories[0].section.value)
        grouped.setdefault(primary, []).append({"id": event.id, "title": event.title, "score": event.importance_score})
    return {"date": day, "sections": grouped}


@router.get("/events/{event_id}")
async def get_event_detail(event_id: int, session: AsyncSession = Depends(get_async_session)) -> dict:
    event = await session.get(Event, event_id)
    if event is None:
        return {"status": "not_found"}

    categories = (await session.execute(select(EventCategory).where(EventCategory.event_id == event_id))).scalars().all()
    tags = (await session.execute(select(EventTag).where(EventTag.event_id == event_id))).scalars().all()
    sources = (await session.execute(select(EventSource).where(EventSource.event_id == event_id))).scalars().all()

    return {
        "event": {
            "id": event.id,
            "event_date": event.event_date,
            "title": event.title,
            "short_summary": event.short_summary,
            "long_summary": event.long_summary,
            "primary_source_id": event.primary_source_id,
            "primary_source_url": event.primary_source_url,
            "importance_score": event.importance_score,
            "confidence_score": event.confidence_score,
        },
        "categories": [
            {"section": category.section.value, "score": category.score, "is_primary_section": category.is_primary_section}
            for category in categories
        ],
        "tags": [{"tag": tag.tag, "tag_type": tag.tag_type.value} for tag in tags],
        "sources": [
            {
                "event_source_id": source.id,
                "source_id": source.source_id,
                "raw_item_id": source.raw_item_id,
                "role": source.role.value,
                "citation_url": source.citation_url,
            }
            for source in sources
        ],
    }
