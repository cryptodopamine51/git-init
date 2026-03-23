from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    Event,
    EventCategory,
    EventSection,
    EventSource,
    EventSourceRole,
    EventTag,
    EventTagType,
    RawItem,
    RawItemStatus,
    Source,
)
from app.services.classification.classifier import ClassificationService
from app.services.clustering.cluster_engine import ClusterEngine
from app.services.normalization.normalizer import NormalizationService
from app.services.scoring.scorer import ScoringService


@dataclass(frozen=True)
class ProcessEventsResult:
    normalized_count: int
    discarded_count: int
    clustered_count: int
    events_created: int
    events_updated: int


class ProcessEventsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.normalizer = NormalizationService()
        self.cluster_engine = ClusterEngine()
        self.classifier = ClassificationService()
        self.scorer = ScoringService()

    async def process(self) -> ProcessEventsResult:
        raw_items = await self._get_fetched_items()
        normalized_count = 0
        discarded_count = 0
        clustered_count = 0
        events_created = 0
        events_updated = 0

        for raw_item in raw_items:
            source = await self.session.get(Source, raw_item.source_id)
            norm = self.normalizer.normalize(raw_item)
            if not norm.is_valid:
                raw_item.status = RawItemStatus.DISCARDED
                discarded_count += 1
                continue

            raw_item.normalized_title = norm.normalized_title
            raw_item.normalized_text = norm.normalized_text
            raw_item.entities_json = norm.entities
            raw_item.outbound_links_json = norm.outbound_links
            raw_item.language = norm.language
            raw_item.status = RawItemStatus.NORMALIZED
            normalized_count += 1

            cluster = self.cluster_engine.build_cluster_decision(raw_item)
            event = await self._get_event_by_cluster(cluster.cluster_key)
            if event is None:
                event = Event(
                    cluster_key=cluster.cluster_key,
                    event_date=(raw_item.published_at.date() if raw_item.published_at else date.today()),
                    title=raw_item.normalized_title or raw_item.raw_title,
                )
                self.session.add(event)
                await self.session.flush()
                events_created += 1
            else:
                events_updated += 1

            await self._attach_event_source(event, raw_item, source)
            await self._recalculate_event(event)

            raw_item.status = RawItemStatus.CLUSTERED
            clustered_count += 1

        await self.session.commit()
        return ProcessEventsResult(
            normalized_count=normalized_count,
            discarded_count=discarded_count,
            clustered_count=clustered_count,
            events_created=events_created,
            events_updated=events_updated,
        )

    async def _get_fetched_items(self) -> list[RawItem]:
        query = select(RawItem).where(RawItem.status == RawItemStatus.FETCHED).order_by(RawItem.published_at.desc().nullslast())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def _get_event_by_cluster(self, cluster_key: str) -> Event | None:
        result = await self.session.execute(select(Event).where(Event.cluster_key == cluster_key))
        return result.scalar_one_or_none()

    async def _attach_event_source(self, event: Event, raw_item: RawItem, source: Source | None) -> None:
        query = select(EventSource).where(EventSource.event_id == event.id, EventSource.raw_item_id == raw_item.id)
        existing = (await self.session.execute(query)).scalar_one_or_none()
        if existing:
            return

        role = EventSourceRole.SUPPORTING
        if source and self._is_better_primary(event, source):
            await self._downgrade_existing_primary(event.id)
            role = EventSourceRole.PRIMARY
            event.primary_source_id = source.id
            event.primary_source_url = raw_item.canonical_url

        self.session.add(
            EventSource(
                event_id=event.id,
                raw_item_id=raw_item.id,
                source_id=raw_item.source_id,
                role=role,
                citation_url=raw_item.canonical_url,
            )
        )

    async def _downgrade_existing_primary(self, event_id: int) -> None:
        query = select(EventSource).where(EventSource.event_id == event_id, EventSource.role == EventSourceRole.PRIMARY)
        existing = (await self.session.execute(query)).scalars().all()
        for item in existing:
            item.role = EventSourceRole.SUPPORTING

    async def _recalculate_event(self, event: Event) -> None:
        source_rows = (
            await self.session.execute(select(EventSource, RawItem, Source).join(RawItem, EventSource.raw_item_id == RawItem.id).join(Source, EventSource.source_id == Source.id).where(EventSource.event_id == event.id))
        ).all()
        if not source_rows:
            return

        primary_row = next((row for row in source_rows if row[0].role == EventSourceRole.PRIMARY), source_rows[0])
        primary_source = primary_row[2]
        primary_raw = primary_row[1]

        event.title = primary_raw.normalized_title or primary_raw.raw_title
        event.event_date = primary_raw.published_at.date() if primary_raw.published_at else event.event_date
        event.short_summary = self._build_short_summary(primary_raw)
        event.long_summary = self._build_long_summary(primary_raw, len(source_rows))

        text_for_classification = f"{event.title} {primary_raw.normalized_text or ''}"
        categories = self.classifier.classify(text_for_classification, primary_source, primary_raw.entities_json or {})
        await self.session.execute(delete(EventCategory).where(EventCategory.event_id == event.id))
        if categories:
            primary_section = max(categories, key=lambda c: c.score).section
            for category in categories:
                self.session.add(
                    EventCategory(
                        event_id=event.id,
                        section=category.section,
                        score=category.score,
                        is_primary_section=category.section == primary_section,
                    )
                )

        tags = self._build_tags(primary_raw.entities_json or {})
        await self.session.execute(delete(EventTag).where(EventTag.event_id == event.id))
        for tag, tag_type in tags:
            self.session.add(EventTag(event_id=event.id, tag=tag, tag_type=tag_type))

        section_map = {c.section: c.score for c in categories}
        scores = self.scorer.score(
            source=primary_source,
            supporting_count=max(len(source_rows) - 1, 0),
            published_at=primary_raw.published_at,
            entities_count=len((primary_raw.entities_json or {}).get("all", [])),
            section_scores=section_map,
        )
        event.importance_score = scores.importance_score
        event.market_impact_score = scores.market_impact_score
        event.ai_news_score = scores.ai_news_score
        event.coding_score = scores.coding_score
        event.investment_score = scores.investment_score
        event.confidence_score = scores.confidence_score
        event.is_highlight = scores.is_highlight

    def _is_better_primary(self, event: Event, candidate_source: Source) -> bool:
        if event.primary_source_id is None:
            return True
        return self._source_rank(candidate_source) > self._current_primary_rank(event)

    def _current_primary_rank(self, event: Event) -> float:
        return 0.0 if event.primary_source_id is None else 1.0

    @staticmethod
    def _source_rank(source: Source) -> float:
        source_type_weight = {
            "official_blog": 3.0,
            "rss_feed": 2.0,
            "website": 1.0,
        }.get(source.source_type.value, 1.0)
        return source_type_weight * 10 + source.priority_weight

    @staticmethod
    def _build_short_summary(raw_item: RawItem) -> str:
        text = raw_item.normalized_text or raw_item.raw_text or raw_item.raw_title
        return (text[:320] + "...") if len(text) > 320 else text

    @staticmethod
    def _build_long_summary(raw_item: RawItem, sources_count: int) -> str:
        text = raw_item.normalized_text or raw_item.raw_text or raw_item.raw_title
        base = (text[:900] + "...") if len(text) > 900 else text
        return f"{base}\n\nCoverage count: {sources_count}."

    @staticmethod
    def _build_tags(entities: dict[str, list[str]]) -> list[tuple[str, EventTagType]]:
        result: list[tuple[str, EventTagType]] = []
        for entity in entities.get("all", [])[:8]:
            result.append((entity[:120], EventTagType.ENTITY))
        for tech_tag in ["llm", "agent", "inference"]:
            result.append((tech_tag, EventTagType.TECH))
        return result
