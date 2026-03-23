from datetime import datetime, timezone

from sqlalchemy import select

from app.api.main import app
from app.db.models import (
    Event,
    EventCategory,
    EventSection,
    EventSource,
    EventSourceRole,
    RawItem,
    RawItemStatus,
    SourceType,
)
from app.services.events.process_events import ProcessEventsService
from app.services.sources.registry import SourceRegistryService, SourceSeedItem


async def _create_source(db_session, title: str, source_type: SourceType, priority: int, section_bias: dict | None = None):
    return await SourceRegistryService(db_session).create_source(
        SourceSeedItem(
            source_type=source_type,
            title=title,
            handle_or_url=f"https://example.com/{title.lower().replace(' ', '-')}",
            priority_weight=priority,
            meta_json={"section_bias": section_bias or {}},
        )
    )


async def _create_raw_item(db_session, source_id: int, ext: str, title: str, text: str, url: str):
    item = RawItem(
        source_id=source_id,
        external_id=ext,
        source_type=SourceType.RSS_FEED,
        author_name="Author",
        published_at=datetime(2026, 3, 23, 10, tzinfo=timezone.utc),
        canonical_url=url,
        raw_title=title,
        raw_text=text,
        raw_payload_json={"id": ext},
        language="en",
        status=RawItemStatus.FETCHED,
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item


async def test_normalization_raw_item(db_session):
    source = await _create_source(db_session, "S1", SourceType.RSS_FEED, 5)
    item = await _create_raw_item(
        db_session,
        source.id,
        "a1",
        "OpenAI launches GPT model",
        "OpenAI announced GPT-X. Details at https://openai.com/blog",
        "https://news.example.com/openai-gpt",
    )

    result = await ProcessEventsService(db_session).process()
    await db_session.refresh(item)

    assert result.normalized_count == 1
    assert item.status == RawItemStatus.CLUSTERED
    assert item.normalized_title


async def test_entity_and_outbound_extraction(db_session):
    source = await _create_source(db_session, "S2", SourceType.RSS_FEED, 5)
    item = await _create_raw_item(
        db_session,
        source.id,
        "a2",
        "Google DeepMind update",
        "Google DeepMind announced Gemini API with OpenAI compatibility https://example.org/post",
        "https://news.example.com/google",
    )

    await ProcessEventsService(db_session).process()
    await db_session.refresh(item)

    assert "Google" in " ".join(item.entities_json.get("all", []))
    assert item.outbound_links_json


async def test_cluster_similar_raw_items_into_one_event(db_session):
    source1 = await _create_source(db_session, "Official", SourceType.OFFICIAL_BLOG, 8)
    source2 = await _create_source(db_session, "Media", SourceType.RSS_FEED, 4)

    await _create_raw_item(db_session, source1.id, "c1", "Anthropic launches model", "Anthropic launched Claude new model", "https://anthropic.com/news/claude")
    await _create_raw_item(db_session, source2.id, "c2", "Claude model release", "Coverage of Anthropic Claude model", "https://anthropic.com/news/claude?ref=media")

    await ProcessEventsService(db_session).process()
    events = (await db_session.execute(select(Event))).scalars().all()

    assert len(events) == 1


async def test_split_different_raw_items_into_different_events(db_session):
    source = await _create_source(db_session, "General", SourceType.RSS_FEED, 5)
    await _create_raw_item(db_session, source.id, "d1", "Startup raised funding", "AI startup raised funding", "https://a.example.com")
    await _create_raw_item(db_session, source.id, "d2", "New coding SDK", "A new Python SDK for agents", "https://b.example.com")

    await ProcessEventsService(db_session).process()
    events = (await db_session.execute(select(Event))).scalars().all()

    assert len(events) == 2


async def test_primary_source_selection(db_session):
    official = await _create_source(db_session, "Official", SourceType.OFFICIAL_BLOG, 9)
    website = await _create_source(db_session, "Website", SourceType.WEBSITE, 3)
    await _create_raw_item(db_session, website.id, "e1", "News on product", "Some article", "https://event.example.com/1")
    await _create_raw_item(db_session, official.id, "e2", "Official post", "Official details", "https://event.example.com/1?official=1")

    await ProcessEventsService(db_session).process()
    event = (await db_session.execute(select(Event))).scalars().one()

    assert event.primary_source_id == official.id
    primary_links = (
        await db_session.execute(select(EventSource).where(EventSource.event_id == event.id, EventSource.role == EventSourceRole.PRIMARY))
    ).scalars().all()
    assert len(primary_links) == 1


async def test_category_assignment(db_session):
    source = await _create_source(db_session, "Biased", SourceType.RSS_FEED, 6, section_bias={"coding": 0.9})
    await _create_raw_item(
        db_session,
        source.id,
        "f1",
        "Python SDK for LLM agents",
        "New SDK for coding with AI and API integrations",
        "https://code.example.com/sdk",
    )
    await ProcessEventsService(db_session).process()

    categories = (await db_session.execute(select(EventCategory))).scalars().all()
    sections = {c.section for c in categories}

    assert EventSection.AI_NEWS in sections
    assert EventSection.CODING in sections


async def test_score_calculation(db_session):
    source = await _create_source(db_session, "Official", SourceType.OFFICIAL_BLOG, 8)
    await _create_raw_item(
        db_session,
        source.id,
        "g1",
        "Major AI regulation update",
        "Major policy and regulation changes for AI market",
        "https://reg.example.com",
    )

    await ProcessEventsService(db_session).process()
    event = (await db_session.execute(select(Event))).scalars().one()

    assert event.importance_score > 0
    assert event.confidence_score > 0


async def test_internal_events_preview_endpoints(api_client, db_session):
    source = await _create_source(db_session, "Preview", SourceType.RSS_FEED, 5)
    await _create_raw_item(db_session, source.id, "h1", "AI news", "Some AI update", "https://preview.example.com")
    await ProcessEventsService(db_session).process()
    event = (await db_session.execute(select(Event))).scalars().one()

    list_resp = await api_client.get("/internal/events")
    detail_resp = await api_client.get(f"/internal/events/{event.id}")
    preview_resp = await api_client.get("/internal/events/preview/day/2026-03-23")

    assert list_resp.status_code == 200
    assert detail_resp.status_code == 200
    assert preview_resp.status_code == 200


async def test_repeated_process_run_is_idempotent(db_session):
    source = await _create_source(db_session, "Idempotent", SourceType.RSS_FEED, 5)
    await _create_raw_item(db_session, source.id, "i1", "Stable event", "Stable event body", "https://stable.example.com")

    service = ProcessEventsService(db_session)
    await service.process()
    await service.process()

    events = (await db_session.execute(select(Event))).scalars().all()
    assert len(events) == 1


async def test_manual_process_events_endpoint(api_client, db_session):
    source = await _create_source(db_session, "Manual", SourceType.RSS_FEED, 5)
    await _create_raw_item(db_session, source.id, "j1", "Manual run", "Manual process run text", "https://manual.example.com")

    response = await api_client.post("/internal/jobs/process-events")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
