from __future__ import annotations

import re
from dataclasses import dataclass

from app.db.models import RawItem

URL_PATTERN = re.compile(r"https?://[^\s)\]>\"]+")
ENTITY_PATTERN = re.compile(r"\b([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+){0,2})\b")
WHITESPACE_PATTERN = re.compile(r"\s+")


@dataclass(frozen=True)
class NormalizationResult:
    normalized_title: str
    normalized_text: str
    outbound_links: list[str]
    entities: dict[str, list[str]]
    language: str
    is_valid: bool


class NormalizationService:
    def normalize(self, raw_item: RawItem) -> NormalizationResult:
        title = self._cleanup(raw_item.raw_title or "")
        body = self._cleanup(raw_item.raw_text or "")
        text = f"{title}. {body}".strip(" .")

        links = sorted(set(URL_PATTERN.findall(raw_item.raw_text or "") + URL_PATTERN.findall(raw_item.canonical_url or "")))
        entities = self._extract_entities(text)
        language = self._resolve_language(raw_item.language, text)
        is_valid = bool(title) and len(text) >= 20

        return NormalizationResult(
            normalized_title=title or "Untitled",
            normalized_text=text,
            outbound_links=links,
            entities=entities,
            language=language,
            is_valid=is_valid,
        )

    @staticmethod
    def _cleanup(value: str) -> str:
        cleaned = value.replace("\n", " ").replace("\t", " ").strip()
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        cleaned = WHITESPACE_PATTERN.sub(" ", cleaned)
        return cleaned.strip()

    def _extract_entities(self, text: str) -> dict[str, list[str]]:
        matches = ENTITY_PATTERN.findall(text)
        unique = sorted({m.strip() for m in matches if len(m.strip()) > 2})

        companies = [e for e in unique if any(token in e.lower() for token in ("ai", "labs", "inc", "corp", "openai", "google", "meta"))]
        people = [e for e in unique if len(e.split()) >= 2 and e not in companies]
        organizations = [e for e in unique if e.endswith("University") or e.endswith("Institute")]
        products = [e for e in unique if any(token in e.lower() for token in ("gpt", "claude", "gemini", "copilot"))]
        models = [e for e in unique if any(token in e.lower() for token in ("gpt", "llama", "mistral", "claude"))]

        return {
            "companies": companies[:15],
            "models": models[:15],
            "products": products[:15],
            "people": people[:15],
            "organizations": organizations[:15],
            "all": unique[:20],
        }

    @staticmethod
    def _resolve_language(raw_language: str | None, text: str) -> str:
        if raw_language:
            return raw_language
        return "ru" if re.search(r"[А-Яа-я]", text) else "en"
