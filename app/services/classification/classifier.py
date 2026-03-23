from __future__ import annotations

from dataclasses import dataclass

from app.db.models import EventSection, Source
from app.services.classification.rules import SECTION_BIAS_MULTIPLIER, SECTION_KEYWORDS


@dataclass(frozen=True)
class CategoryScore:
    section: EventSection
    score: float


class ClassificationService:
    def classify(self, text: str, source: Source | None, entities: dict[str, list[str]] | None) -> list[CategoryScore]:
        lowered = text.lower()
        scores: dict[EventSection, float] = {
            EventSection.IMPORTANT: 0.0,
            EventSection.AI_NEWS: 0.0,
            EventSection.CODING: 0.0,
            EventSection.INVESTMENTS: 0.0,
            EventSection.ALPHA: 0.0,
        }

        mapping = {
            EventSection.IMPORTANT: "important",
            EventSection.AI_NEWS: "ai_news",
            EventSection.CODING: "coding",
            EventSection.INVESTMENTS: "investments",
        }

        for section, key in mapping.items():
            for keyword in SECTION_KEYWORDS[key]:
                if keyword in lowered:
                    scores[section] += 0.2

        if entities:
            density = min(len(entities.get("all", [])) * 0.03, 0.3)
            scores[EventSection.IMPORTANT] += density
            scores[EventSection.AI_NEWS] += density / 2

        if source and source.meta_json:
            section_bias = source.meta_json.get("section_bias", {})
            for section, bias in section_bias.items():
                for enum_value in EventSection:
                    if enum_value.value == section:
                        scores[enum_value] += float(bias) * SECTION_BIAS_MULTIPLIER

        primary_section = max(scores, key=scores.get)
        if scores[primary_section] <= 0:
            scores[EventSection.AI_NEWS] = 0.2

        return [CategoryScore(section=sec, score=round(val, 4)) for sec, val in scores.items() if val > 0]
