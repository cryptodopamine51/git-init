from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class IngestedItem:
    external_id: str
    published_at: datetime | None
    canonical_url: str
    title: str
    text: str | None
    author_name: str | None
    language: str | None
    payload: dict
