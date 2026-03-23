from abc import ABC, abstractmethod

from app.db.models import Source
from app.services.ingestion.schemas import IngestedItem


class SourceAdapter(ABC):
    @abstractmethod
    async def fetch(self, source: Source) -> list[IngestedItem]:
        raise NotImplementedError
