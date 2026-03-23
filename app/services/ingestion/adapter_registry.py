from app.db.models import SourceType
from app.services.ingestion.adapters.base import SourceAdapter
from app.services.ingestion.adapters.json_feed import JsonFeedAdapter
from app.services.ingestion.adapters.rss_atom import RssAtomAdapter


class AdapterRegistry:
    def __init__(self) -> None:
        rss_adapter = RssAtomAdapter()
        self._registry: dict[SourceType, SourceAdapter] = {
            SourceType.RSS_FEED: rss_adapter,
            SourceType.OFFICIAL_BLOG: rss_adapter,
            SourceType.WEBSITE: JsonFeedAdapter(),
        }

    def get_adapter(self, source_type: SourceType) -> SourceAdapter:
        if source_type not in self._registry:
            raise ValueError(f"No adapter for source_type={source_type}")
        return self._registry[source_type]
