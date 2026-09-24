#!/usr/bin/env python3
"""Check hard word limits for current .workflow project documents."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LIMITS = {
    "direction": 800,
    "backlog": 1800,
    "backlog_item": 80,
    "context": 1500,
    "context_entry": 80,
    "feature_brief": 1000,
    "acceptance_report": 800,
    "pdr": 500,
    "adr": 700,
}

HEADING = re.compile(r"^## (.+?)\s*$")


def word_count(text: str) -> int:
    """Count whitespace-separated words in Markdown source, including headings."""
    return len(text.split())


def records(markdown: str) -> list[tuple[str, str]]:
    """Return level-two Markdown sections as named records."""
    result: list[tuple[str, str]] = []
    title: str | None = None
    lines: list[str] = []
    for line in markdown.splitlines():
        match = HEADING.match(line)
        if match:
            if title is not None:
                result.append((title, "\n".join(lines)))
            title = match.group(1)
            lines = [line]
        elif title is not None:
            lines.append(line)
    if title is not None:
        result.append((title, "\n".join(lines)))
    return result


def check_file(path: Path, limit: int, label: str) -> list[str]:
    if not path.is_file():
        return []
    count = word_count(path.read_text(encoding="utf-8"))
    if count > limit:
        return [f"{path}: {count} words in {label}; hard limit {limit}"]
    return []


def check_records(path: Path, limit: int, label: str) -> list[str]:
    if not path.is_file():
        return []
    findings = []
    for title, body in records(path.read_text(encoding="utf-8")):
        count = word_count(body)
        if count > limit:
            findings.append(
                f"{path}: {label} '{title}' has {count} words; hard limit {limit}"
            )
    return findings


def check(root: Path) -> list[str]:
    workflow = root / ".workflow"
    findings = []
    findings.extend(check_file(workflow / "direction.md", LIMITS["direction"], "Direction"))
    for name, record_limit, record_label in (
        ("backlog", LIMITS["backlog_item"], "Backlog item"),
        ("context", LIMITS["context_entry"], "Context entry"),
    ):
        path = workflow / f"{name}.md"
        findings.extend(check_file(path, LIMITS[name], name.title()))
        findings.extend(check_records(path, record_limit, record_label))
    for path in sorted((workflow / "decisions" / "pdr").glob("*.md")):
        findings.extend(check_file(path, LIMITS["pdr"], "PDR"))
    for path in sorted((workflow / "decisions" / "adr").glob("*.md")):
        findings.extend(check_file(path, LIMITS["adr"], "ADR"))
    for path in sorted((workflow / "features").glob("*/brief.md")):
        findings.extend(check_file(path, LIMITS["feature_brief"], "Feature Brief"))
    for path in sorted((workflow / "features").glob("*/acceptance-*.md")):
        findings.extend(check_file(path, LIMITS["acceptance_report"], "Acceptance Report"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if not args.project_root.is_dir():
        parser.error(f"not a directory: {args.project_root}")
    findings = check(args.project_root)
    if findings:
        print("\n".join(findings))
        return 1
    print("Workflow document sizes are within hard limits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
