import asyncio

from app.db.models import SourceType
from app.db.session import SessionLocal
from app.services.sources.registry import SourceRegistryService, SourceSeedItem

DEFAULT_SOURCES = [
    SourceSeedItem(
        source_type=SourceType.RSS_FEED,
        title="OpenAI Blog",
        handle_or_url="https://openai.com/news/rss.xml",
        language="en",
        country_scope="global",
        priority_weight=5,
    ),
    SourceSeedItem(
        source_type=SourceType.OFFICIAL_BLOG,
        title="Anthropic News",
        handle_or_url="https://www.anthropic.com/news/rss.xml",
        language="en",
        country_scope="global",
        priority_weight=4,
    ),
]


async def main() -> None:
    async with SessionLocal() as session:
        inserted = await SourceRegistryService(session).upsert_sources(DEFAULT_SOURCES)
    print(f"Inserted sources: {inserted}")


if __name__ == "__main__":
    asyncio.run(main())
