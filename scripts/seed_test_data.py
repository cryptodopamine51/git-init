import asyncio

from app.db.models import SourceType
from app.db.session import SessionLocal
from app.services.sources.registry import SourceRegistryService, SourceSeedItem


async def main() -> None:
    test_source = SourceSeedItem(
        source_type=SourceType.WEBSITE,
        title="Local JSON Feed",
        handle_or_url="http://localhost:9000/feed.json",
        language="en",
        country_scope="global",
        priority_weight=1,
    )
    async with SessionLocal() as session:
        inserted = await SourceRegistryService(session).upsert_sources([test_source])
    print(f"Inserted test sources: {inserted}")


if __name__ == "__main__":
    asyncio.run(main())
