"""Derive STE vocabulary from agreed project Context entries."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml


CLASSES = {
    "technical name": "technical_nouns",
    "technical verb": "technical_verbs",
}


def context_entries(markdown: str) -> list[tuple[str, str, str, list[str]]]:
    """Read Context entries with a meaning, STE class, and optional forms."""
    entries = []
    term = None
    fields: dict[str, str] = {}
    last_field = None

    def finish() -> None:
        if term is None:
            return
        meaning = fields.get("meaning", "").strip()
        classification = fields.get("ste class", "").strip().casefold()
        if not meaning or classification not in CLASSES:
            raise ValueError(f"Context term '{term}' needs Meaning and STE class")
        forms = [form.strip() for form in fields.get("forms", "").split(",") if form.strip()]
        entries.append((term, meaning, CLASSES[classification], forms))

    for line in markdown.splitlines():
        if line.startswith("## "):
            finish()
            term = line[3:].strip()
            if not term:
                raise ValueError("Context has an empty term heading")
            fields = {}
            last_field = None
            continue
        if term is None:
            continue
        if line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            key = key.strip().casefold()
            if key == "status" and value.strip().casefold() not in {"agreed", "accepted"}:
                raise ValueError(f"Context term '{term}' is not agreed")
            if key in {"meaning", "ste class", "forms"}:
                if key in fields:
                    raise ValueError(f"Context term '{term}' repeats {key}")
                fields[key] = value.strip()
                last_field = key
            else:
                last_field = None
        elif line.startswith("  ") and last_field:
            fields[last_field] += " " + line.strip()
        elif line.strip():
            last_field = None
    finish()
    return entries


def combined_glossary(shared_path: Path, context_path: Path) -> dict:
    """Merge shared vocabulary and agreed Context terms in memory."""
    with shared_path.open(encoding="utf-8") as source:
        shared = yaml.safe_load(source)
    if not isinstance(shared, dict):
        raise ValueError("Shared STE vocabulary is not a mapping")
    glossary = deepcopy(shared)
    used = set()
    for category in CLASSES.values():
        values = glossary.get(category, [])
        if not isinstance(values, list):
            raise ValueError(f"Shared STE {category} is not a list")
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("word"), str):
                raise ValueError(f"Shared STE {category} has an invalid entry")
            used.add(item["word"].casefold())
            used.update(str(form).casefold() for form in item.get("inflections", []))
        glossary[category] = values
    preferred = glossary.get("preferred_terms", {})
    if not isinstance(preferred, dict):
        raise ValueError("Shared STE preferred terms are not a mapping")
    used.update(str(word).casefold() for word in preferred)

    for term, meaning, category, forms in context_entries(
        context_path.read_text(encoding="utf-8")
    ):
        for word in (term, *forms):
            key = word.casefold()
            if key in used:
                raise ValueError(f"Context term or form '{word}' conflicts with existing vocabulary")
            used.add(key)
        glossary[category].append(
            {"word": term, "approved_meaning": meaning, "inflections": forms}
        )
    return glossary
