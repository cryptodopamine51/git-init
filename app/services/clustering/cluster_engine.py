from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date

from app.db.models import RawItem


@dataclass(frozen=True)
class ClusterDecision:
    cluster_key: str
    similarity_score: float


class ClusterEngine:
    def build_cluster_decision(self, item: RawItem) -> ClusterDecision:
        canonical_basis = (item.canonical_url or "").split("?")[0].strip().lower()
        title_tokens = self._tokenize(item.normalized_title or item.raw_title or "")[:8]
        entity_tokens = (item.entities_json or {}).get("all", [])[:4]
        date_part = (item.published_at.date() if item.published_at else date.today()).isoformat()

        if canonical_basis:
            base = f"url:{canonical_basis}"
        else:
            base = f"txt:{' '.join(title_tokens)}|{' '.join(entity_tokens)}|{date_part}"

        cluster_key = hashlib.sha1(base.encode("utf-8")).hexdigest()
        similarity_score = self._estimate_similarity(title_tokens, entity_tokens)
        return ClusterDecision(cluster_key=cluster_key, similarity_score=similarity_score)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [t for t in ''.join(ch if ch.isalnum() else ' ' for ch in text.lower()).split() if len(t) > 2]

    @staticmethod
    def _estimate_similarity(title_tokens: list[str], entity_tokens: list[str]) -> float:
        if not title_tokens:
            return 0.2
        overlap_bonus = min(len(set(title_tokens) & set(t.lower() for t in entity_tokens)) * 0.1, 0.4)
        return min(0.5 + overlap_bonus, 0.95)
