from datetime import datetime
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

import httpx

from app.db.models import Source
from app.services.ingestion.adapters.base import SourceAdapter
from app.services.ingestion.schemas import IngestedItem


class RssAtomAdapter(SourceAdapter):
    async def fetch(self, source: Source) -> list[IngestedItem]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(source.handle_or_url)
            response.raise_for_status()

        root = ElementTree.fromstring(response.text)
        channel = root.find("channel")
        if channel is not None:
            entries = channel.findall("item")
            return [self._from_rss_entry(entry, source.language) for entry in entries]

        entries = root.findall("{http://www.w3.org/2005/Atom}entry")
        return [self._from_atom_entry(entry, source.language) for entry in entries]

    def _from_rss_entry(self, entry: ElementTree.Element, fallback_language: str | None) -> IngestedItem:
        guid = self._text(entry, "guid") or self._text(entry, "link")
        if not guid:
            raise ValueError("RSS entry missing guid/link")

        return IngestedItem(
            external_id=guid,
            published_at=self._parse_dt(self._text(entry, "pubDate")),
            canonical_url=self._text(entry, "link") or guid,
            title=self._text(entry, "title") or "Untitled",
            text=self._text(entry, "description"),
            author_name=self._text(entry, "author"),
            language=fallback_language,
            payload={"raw": ElementTree.tostring(entry, encoding="unicode")},
        )

    def _from_atom_entry(self, entry: ElementTree.Element, fallback_language: str | None) -> IngestedItem:
        atom_ns = "{http://www.w3.org/2005/Atom}"
        external_id = self._text(entry, f"{atom_ns}id")
        link_node = entry.find(f"{atom_ns}link")
        canonical_url = (link_node.attrib.get("href") if link_node is not None else None) or external_id
        if not external_id or not canonical_url:
            raise ValueError("Atom entry missing id/link")

        return IngestedItem(
            external_id=external_id,
            published_at=self._parse_dt(self._text(entry, f"{atom_ns}published") or self._text(entry, f"{atom_ns}updated")),
            canonical_url=canonical_url,
            title=self._text(entry, f"{atom_ns}title") or "Untitled",
            text=self._text(entry, f"{atom_ns}summary"),
            author_name=self._text(entry, f"{atom_ns}author/{atom_ns}name"),
            language=fallback_language,
            payload={"raw": ElementTree.tostring(entry, encoding="unicode")},
        )

    @staticmethod
    def _text(node: ElementTree.Element, path: str) -> str | None:
        found = node.find(path)
        return found.text.strip() if found is not None and found.text else None

    @staticmethod
    def _parse_dt(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return parsedate_to_datetime(value)
        except Exception:
            return None
