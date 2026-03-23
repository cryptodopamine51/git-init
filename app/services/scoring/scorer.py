from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.db.models import EventSection, Source, SourceType
from app.services.scoring.config import SCORE_WEIGHTS, SECTION_SCORE_WEIGHTS


@dataclass(frozen=True)
class ScoreResult:
    importance_score: float
    market_impact_score: float
    ai_news_score: float
    coding_score: float
    investment_score: float
    confidence_score: float
    is_highlight: bool


class ScoringService:
    def score(
        self,
        source: Source | None,
        supporting_count: int,
        published_at: datetime | None,
        entities_count: int,
        section_scores: dict[EventSection, float],
    ) -> ScoreResult:
        source_priority = float(source.priority_weight if source else 1)
        source_component = min(source_priority / 10.0, 1.0) * SCORE_WEIGHTS["source_priority"]
        supporting_component = min(supporting_count / 5.0, 1.0) * SCORE_WEIGHTS["supporting_sources"]
        entity_component = min(entities_count / 12.0, 1.0) * SCORE_WEIGHTS["entity_density"]
        freshness_component = self._freshness_component(published_at) * SCORE_WEIGHTS["freshness"]
        official_component = (1.0 if source and source.source_type == SourceType.OFFICIAL_BLOG else 0.0) * SCORE_WEIGHTS[
            "official_bonus"
        ]

        importance = min(source_component + supporting_component + entity_component + freshness_component + official_component, 1.0)

        ai_news = min(section_scores.get(EventSection.AI_NEWS, 0.0) * SECTION_SCORE_WEIGHTS["ai_news"] + importance * 0.2, 1.0)
        coding = min(section_scores.get(EventSection.CODING, 0.0) * SECTION_SCORE_WEIGHTS["coding"], 1.0)
        investment = min(section_scores.get(EventSection.INVESTMENTS, 0.0) * SECTION_SCORE_WEIGHTS["investments"], 1.0)
        market_impact = min((investment * 0.6 + importance * 0.4), 1.0)
        confidence = min(0.4 + supporting_component + entity_component + freshness_component, 1.0)
        is_highlight = importance >= 0.72

        return ScoreResult(
            importance_score=round(importance, 4),
            market_impact_score=round(market_impact, 4),
            ai_news_score=round(ai_news, 4),
            coding_score=round(coding, 4),
            investment_score=round(investment, 4),
            confidence_score=round(confidence, 4),
            is_highlight=is_highlight,
        )

    @staticmethod
    def _freshness_component(published_at: datetime | None) -> float:
        if published_at is None:
            return 0.4
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        delta_hours = max((datetime.now(timezone.utc) - published_at).total_seconds() / 3600.0, 0)
        if delta_hours <= 24:
            return 1.0
        if delta_hours <= 72:
            return 0.7
        return 0.3
