"""Combine shared, project, and Context STE vocabulary."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


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


def project_entries(path: Path) -> list[tuple[str, dict]]:
    """Read approved domain terms without project definitions."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) - set(CLASSES.values()):
        raise ValueError(f"Project glossary has invalid fields: {path}")
    entries = []
    for category in CLASSES.values():
        values = raw.get(category, [])
        if not isinstance(values, list):
            raise ValueError(f"Project glossary {category} must be a list")
        for value in values:
            if isinstance(value, str):
                word, forms = value, []
            elif isinstance(value, dict) and set(value) <= {"word", "inflections"}:
                word, forms = value.get("word"), value.get("inflections", [])
            else:
                raise ValueError(f"Invalid project glossary entry: {value!r}")
            if not isinstance(word, str) or not word.strip():
                raise ValueError("Project glossary entries need a word")
            if not isinstance(forms, list) or any(
                not isinstance(form, str) or not form.strip() for form in forms
            ):
                raise ValueError(f"Project glossary forms for '{word}' must be words")
            entries.append(
                (category, {"word": word.strip(), "inflections": [form.strip() for form in forms]})
            )
    return entries


def combined_glossary(
    shared_path: Path, context_path: Path | None = None, project_path: Path | None = None
) -> dict:
    """Merge the available vocabulary sources in memory."""
    with shared_path.open(encoding="utf-8") as source:
        shared = json.load(source)
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

    if project_path is not None:
        for category, entry in project_entries(project_path):
            for word in (entry["word"], *entry["inflections"]):
                key = word.casefold()
                if key in used:
                    raise ValueError(
                        f"Project glossary term or form '{word}' conflicts with existing vocabulary"
                    )
                used.add(key)
            glossary[category].append(entry)

    if context_path is None:
        return glossary
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
