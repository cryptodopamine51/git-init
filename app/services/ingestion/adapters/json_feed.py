from datetime import datetime

import httpx

from app.db.models import Source
from app.services.ingestion.adapters.base import SourceAdapter
from app.services.ingestion.schemas import IngestedItem


class JsonFeedAdapter(SourceAdapter):
    async def fetch(self, source: Source) -> list[IngestedItem]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(source.handle_or_url)
            response.raise_for_status()
        payload = response.json()
        items = payload.get("items", [])
        results: list[IngestedItem] = []
        for item in items:
            external_id = item.get("id") or item.get("url")
            canonical_url = item.get("url")
            title = item.get("title")
            if not external_id or not canonical_url or not title:
                continue
            results.append(
                IngestedItem(
                    external_id=str(external_id),
                    published_at=self._parse_datetime(item.get("published_at")),
                    canonical_url=str(canonical_url),
                    title=str(title),
                    text=item.get("text"),
                    author_name=item.get("author_name"),
                    language=item.get("language") or source.language,
                    payload=item,
                )
            )
        return results

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
