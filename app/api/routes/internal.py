from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RawItem, SourceRun
from app.db.session import get_async_session
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
