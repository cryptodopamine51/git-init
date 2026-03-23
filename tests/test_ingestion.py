from app.api.main import app
from datetime import datetime, timezone

from sqlalchemy import select

from app.db.models import RawItem, Source, SourceRun, SourceRunStatus, SourceType
from app.services.ingestion.adapter_registry import AdapterRegistry
from app.services.ingestion.ingestion_service import IngestionService
from app.services.ingestion.schemas import IngestedItem
from app.services.sources.registry import SourceRegistryService, SourceSeedItem


class FakeSuccessAdapter:
    async def fetch(self, source: Source) -> list[IngestedItem]:
        return [
            IngestedItem(
                external_id="item-1",
                published_at=datetime(2026, 3, 20, tzinfo=timezone.utc),
                canonical_url="https://example.com/1",
                title="First",
                text="Body",
                author_name="Author",
                language="en",
                payload={"id": "item-1"},
            )
        ]


class FakeFailedAdapter:
    async def fetch(self, source: Source) -> list[IngestedItem]:
        raise RuntimeError("adapter failure")


async def _create_source(db_session, source_type: SourceType = SourceType.RSS_FEED) -> Source:
    return await SourceRegistryService(db_session).create_source(
        SourceSeedItem(
            source_type=source_type,
            title="Test Source",
            handle_or_url=f"https://example.com/{source_type.value}",
        )
    )


async def test_create_sources(db_session):
    await SourceRegistryService(db_session).create_source(
        SourceSeedItem(source_type=SourceType.RSS_FEED, title="A", handle_or_url="https://example.com/a.xml")
    )
    sources = await SourceRegistryService(db_session).list_sources()
    assert len(sources) == 1


async def test_successful_ingestion_rss_source(db_session):
    source = await _create_source(db_session)
    adapters = AdapterRegistry()
    adapters._registry[source.source_type] = FakeSuccessAdapter()  # noqa: SLF001

    run = await IngestionService(db_session, adapters).run_source(source)
    items = (await db_session.execute(select(RawItem))).scalars().all()

    assert run.status == SourceRunStatus.SUCCESS
    assert run.inserted_count == 1
    assert len(items) == 1


async def test_dedup_on_repeated_run(db_session):
    source = await _create_source(db_session)
    adapters = AdapterRegistry()
    adapters._registry[source.source_type] = FakeSuccessAdapter()  # noqa: SLF001
    service = IngestionService(db_session, adapters)

    first = await service.run_source(source)
    second = await service.run_source(source)
    items = (await db_session.execute(select(RawItem))).scalars().all()

    assert first.inserted_count == 1
    assert second.inserted_count == 0
    assert len(items) == 1


async def test_source_run_success_logging(db_session):
    source = await _create_source(db_session)
    adapters = AdapterRegistry()
    adapters._registry[source.source_type] = FakeSuccessAdapter()  # noqa: SLF001

    await IngestionService(db_session, adapters).run_source(source)
    runs = (await db_session.execute(select(SourceRun))).scalars().all()

    assert len(runs) == 1
    assert runs[0].status == SourceRunStatus.SUCCESS


async def test_source_run_failed_logging(db_session):
    source = await _create_source(db_session)
    adapters = AdapterRegistry()
    adapters._registry[source.source_type] = FakeFailedAdapter()  # noqa: SLF001

    run = await IngestionService(db_session, adapters).run_source(source)

    assert run.status == SourceRunStatus.FAILED
    assert "adapter failure" in (run.error_message or "")


async def test_internal_preview_endpoints(api_client, db_session):
    await _create_source(db_session)

    response = await api_client.get("/internal/sources")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_manual_ingest_endpoint(api_client, db_session):
    source = await _create_source(db_session)
    adapters = AdapterRegistry()
    adapters._registry[source.source_type] = FakeSuccessAdapter()  # noqa: SLF001
    app.state.adapter_registry = adapters

    response = await api_client.post("/internal/jobs/ingest")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["runs"][0]["inserted_count"] == 1
