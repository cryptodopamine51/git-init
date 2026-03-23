from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RawItem, RawItemStatus, Source, SourceRun, SourceRunStatus
from app.services.ingestion.adapter_registry import AdapterRegistry
from app.services.sources.registry import SourceRegistryService


class IngestionService:
    def __init__(self, session: AsyncSession, adapter_registry: AdapterRegistry | None = None) -> None:
        self.session = session
        self.adapter_registry = adapter_registry or AdapterRegistry()

    async def run_all_active_sources(self) -> list[SourceRun]:
        sources = await SourceRegistryService(self.session).list_sources(active_only=True)
        runs: list[SourceRun] = []
        for source in sources:
            run = await self.run_source(source)
            runs.append(run)
        return runs

    async def run_source(self, source: Source) -> SourceRun:
        active_run = await self._get_active_run(source.id)
        if active_run:
            return active_run

        run = SourceRun(source_id=source.id, status=SourceRunStatus.SUCCESS)
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)

        try:
            adapter = self.adapter_registry.get_adapter(source.source_type)
            items = await adapter.fetch(source)
            inserted = await self._insert_new_raw_items(source, items)
            run.fetched_count = len(items)
            run.inserted_count = inserted
            run.status = SourceRunStatus.SUCCESS
            run.finished_at = datetime.now(timezone.utc)
            await self.session.commit()
            await self.session.refresh(run)
            return run
        except Exception as exc:
            run.status = SourceRunStatus.FAILED
            run.error_message = str(exc)
            run.finished_at = datetime.now(timezone.utc)
            await self.session.commit()
            await self.session.refresh(run)
            return run

    async def _insert_new_raw_items(self, source: Source, items: list) -> int:
        if not items:
            return 0

        external_ids = [item.external_id for item in items]
        existing_rows = await self.session.execute(
            select(RawItem.external_id).where(RawItem.source_id == source.id, RawItem.external_id.in_(external_ids))
        )
        existing_external_ids = set(existing_rows.scalars().all())

        inserted = 0
        for item in items:
            if item.external_id in existing_external_ids:
                continue
            self.session.add(
                RawItem(
                    source_id=source.id,
                    external_id=item.external_id,
                    source_type=source.source_type,
                    author_name=item.author_name,
                    published_at=item.published_at,
                    canonical_url=item.canonical_url,
                    raw_title=item.title,
                    raw_text=item.text,
                    raw_payload_json=item.payload,
                    language=item.language,
                    status=RawItemStatus.FETCHED,
                )
            )
            inserted += 1

        if inserted:
            await self.session.commit()
        return inserted

    async def _get_active_run(self, source_id: int) -> SourceRun | None:
        query = select(SourceRun).where(
            SourceRun.source_id == source_id,
            SourceRun.finished_at.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
