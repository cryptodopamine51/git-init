from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Source, SourceType


@dataclass(frozen=True)
class SourceSeedItem:
    source_type: SourceType
    title: str
    handle_or_url: str
    priority_weight: int = 1
    is_active: bool = True
    language: str | None = "en"
    country_scope: str | None = "global"
    meta_json: dict | None = None


class SourceRegistryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_sources(self, active_only: bool = False) -> list[Source]:
        query = select(Source).order_by(Source.priority_weight.desc(), Source.id.asc())
        if active_only:
            query = query.where(Source.is_active.is_(True))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create_source(self, item: SourceSeedItem) -> Source:
        source = Source(
            source_type=item.source_type,
            title=item.title,
            handle_or_url=item.handle_or_url,
            priority_weight=item.priority_weight,
            is_active=item.is_active,
            language=item.language,
            country_scope=item.country_scope,
            meta_json=item.meta_json,
        )
        self.session.add(source)
        await self.session.commit()
        await self.session.refresh(source)
        return source

    async def upsert_sources(self, items: list[SourceSeedItem]) -> int:
        existing_query = await self.session.execute(select(Source.handle_or_url))
        existing_urls = set(existing_query.scalars().all())
        inserted = 0

        for item in items:
            if item.handle_or_url in existing_urls:
                continue
            self.session.add(
                Source(
                    source_type=item.source_type,
                    title=item.title,
                    handle_or_url=item.handle_or_url,
                    priority_weight=item.priority_weight,
                    is_active=item.is_active,
                    language=item.language,
                    country_scope=item.country_scope,
                    meta_json=item.meta_json,
                )
            )
            inserted += 1

        if inserted:
            await self.session.commit()

        return inserted
