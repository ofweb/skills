"""Combine shared, project, and Context STE vocabulary."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


CLASSES = {
    "technical name": "technical_nouns",
    "technical verb": "technical_verbs",
}
PARTS_OF_SPEECH = {"noun", "verb", "adjective"}


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


def approved_entries(raw: dict, *, project: bool) -> list[tuple[str, dict]]:
    """Convert reviewed terms to the pinned checker's glossary format."""
    entries = []
    categories = ("approved_terms", *CLASSES.values())
    for category in categories:
        values = raw.get(category, [])
        if not isinstance(values, list):
            raise ValueError(f"Glossary {category} must be a list")
        for value in values:
            if isinstance(value, str):
                entry = {"word": value}
            elif isinstance(value, dict):
                allowed = {"word", "inflections", "part_of_speech"}
                if not project:
                    allowed.add("approved_meaning")
                if set(value) - allowed:
                    label = "project glossary" if project else "shared glossary"
                    raise ValueError(f"Invalid {label} entry: {value!r}")
                entry = value.copy()
            else:
                raise ValueError(f"Invalid glossary entry: {value!r}")
            word, forms = entry.get("word"), entry.get("inflections", [])
            if not isinstance(word, str) or not word.strip():
                raise ValueError("Glossary entries need a word")
            if not isinstance(forms, list) or any(
                not isinstance(form, str) or not form.strip() for form in forms
            ):
                raise ValueError(f"Glossary forms for '{word}' must be words")
            pos = entry.get("part_of_speech", "verb" if category == "technical_verbs" else "noun")
            if not isinstance(pos, str) or pos not in PARTS_OF_SPEECH:
                raise ValueError(f"Glossary part_of_speech for '{word}' is invalid")
            if category == "technical_nouns" and pos == "verb":
                raise ValueError(f"Glossary category and part_of_speech conflict for '{word}'")
            if category == "technical_verbs" and pos != "verb":
                raise ValueError(f"Glossary category and part_of_speech conflict for '{word}'")
            native = "technical_verbs" if pos == "verb" else "technical_nouns"
            term = {"word": word.strip(), "inflections": [form.strip() for form in forms]}
            if pos == "adjective":
                term["part_of_speech"] = pos
            if "approved_meaning" in entry:
                term["approved_meaning"] = entry["approved_meaning"]
            entries.append((native, term))
    return entries


def project_data(path: Path) -> tuple[list[tuple[str, dict]], list[str]]:
    """Read local terms and exact names without changing shared vocabulary."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) - {"approved_terms", "exact_names", *CLASSES.values()}:
        raise ValueError(f"Project glossary has invalid fields: {path}")
    names = raw.get("exact_names", [])
    if not isinstance(names, list) or any(
        not isinstance(name, str) or not name.strip() for name in names
    ):
        raise ValueError("Project exact_names must be a list of names")
    if any(not any(char.isupper() for char in name) for name in names):
        raise ValueError("Project exact_names need a capitalized exact name; use inline code for IDs")
    return approved_entries(raw, project=True), [name.strip() for name in names]


def project_entries(path: Path) -> list[tuple[str, dict]]:
    """Keep the legacy project-entry reader available to callers."""
    return project_data(path)[0]


def combined_glossary(
    shared_path: Path, context_path: Path | None = None, project_path: Path | None = None
) -> dict:
    """Merge the available vocabulary sources in memory."""
    with shared_path.open(encoding="utf-8") as source:
        shared = json.load(source)
    if not isinstance(shared, dict):
        raise ValueError("Shared STE vocabulary is not a mapping")
    if set(shared) - {"name", "approved_terms", "technical_nouns", "technical_verbs", "preferred_terms"}:
        raise ValueError("Shared STE vocabulary has invalid fields")
    glossary = {
        "name": shared.get("name", "shared-software-prose"),
        "technical_nouns": [],
        "technical_verbs": [],
    }
    glossary["preferred_terms"] = deepcopy(shared.get("preferred_terms", {}))
    for category, entry in approved_entries(shared, project=False):
        glossary[category].append(entry)
    used = set()
    for category in CLASSES.values():
        values = glossary.get(category, [])
        if not isinstance(values, list):
            raise ValueError(f"Shared STE {category} is not a list")
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("word"), str):
                raise ValueError(f"Shared STE {category} has an invalid entry")
            for form in (item["word"], *item.get("inflections", [])):
                key = form.casefold()
                if key in used:
                    raise ValueError(f"Shared STE term or form '{form}' repeats")
                used.add(key)
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
