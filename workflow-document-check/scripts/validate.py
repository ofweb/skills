#!/usr/bin/env python3
"""Validate workflow documents with a Markdown token tree."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from mdit_py_plugins.anchors import anchors_plugin


PARSER = (
    MarkdownIt("commonmark")
    .enable("table")
    .enable("strikethrough")
    .use(anchors_plugin, min_level=1, max_level=6)
)
LIMITS = {
    "direction": 4000,
    "direction_topic": 2000,
    "backlog": 1800,
    "backlog_item": 80,
    "context": 5000,
    "context_entry": 80,
    "feature_brief": 1000,
    "acceptance_report": 800,
    "pdr": 500,
    "adr": 700,
}
REQUIRED = ("Goal", "Stories and acceptance", "Scope", "Non-goals")
STATUSES = ("Draft", "Ready", "Designed", "Implemented", "Reviewed", "Accepted")
NAMED_SECTIONS = set(REQUIRED) | {
    "Feature-wide constraints and acceptance",
    "Related records",
    "Open questions and assumptions",
}
FEATURE_ID = re.compile(r"B-\d{4}\Z")
STORY_ID = re.compile(r"S([1-9]\d*):\s+\S")
BACKLOG_ID = re.compile(r"(B-\d{4}):\s+\S")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    line: int
    message: str
    warning: bool = False


@dataclass
class Document:
    file: Path
    path: str
    source: str
    lines: list[str]
    tree: SyntaxTreeNode


@dataclass
class Section:
    name: str
    heading: SyntaxTreeNode
    nodes: list[SyntaxTreeNode]


def parse(root: Path, file: Path) -> Document:
    source = file.read_text(encoding="utf-8")
    try:
        name = file.relative_to(root).as_posix()
    except ValueError:
        name = file.as_posix()
    return Document(
        file,
        name,
        source,
        source.splitlines(),
        SyntaxTreeNode(PARSER.parse(source)),
    )


def line(node: SyntaxTreeNode) -> int:
    return node.map[0] + 1 if node.map else 1


def depth(node: SyntaxTreeNode) -> int:
    return int(node.tag[1])


def text(node: SyntaxTreeNode) -> str:
    if node.type in {"text", "code_inline", "html_inline"}:
        return node.content
    if node.type in {"softbreak", "hardbreak"}:
        return " "
    return "".join(text(child) for child in node.children)


def sections(doc: Document) -> list[Section]:
    result: list[Section] = []
    current: Section | None = None
    for node in doc.tree.children:
        if node.type == "heading" and depth(node) == 2:
            current = Section(text(node), node, [])
            result.append(current)
        elif current is not None:
            current.nodes.append(node)
    return result


def add(
    findings: list[Finding],
    code: str,
    path: str,
    at: int,
    message: str,
    warning: bool = False,
) -> None:
    findings.append(Finding(code, path, at, message, warning))


def complete(
    findings: list[Finding],
    status: str,
    code: str,
    path: str,
    at: int,
    message: str,
) -> None:
    add(findings, code, path, at, message, status == "Draft")


def word_count(source: str) -> int:
    return len(source.split())


def check_size(doc: Document, findings: list[Finding], limit: int, label: str) -> None:
    count = word_count(doc.source)
    if count > limit:
        add(
            findings,
            "SIZE001",
            doc.path,
            1,
            f"{label} has {count} words; hard limit {limit}",
        )


def check_records(
    doc: Document, findings: list[Finding], limit: int, label: str
) -> None:
    parts = sections(doc)
    for index, part in enumerate(parts):
        start = part.heading.map[0]
        end = parts[index + 1].heading.map[0] if index + 1 < len(parts) else len(doc.lines)
        count = word_count("\n".join(doc.lines[start:end]))
        if count > limit:
            add(
                findings,
                "SIZE002",
                doc.path,
                line(part.heading),
                f"{label} '{part.name}' has {count} words; hard limit {limit}",
            )


def preamble_fields(doc: Document) -> dict[str, list[tuple[str, int]]]:
    first_h2 = next(
        (
            index
            for index, node in enumerate(doc.tree.children)
            if node.type == "heading" and depth(node) == 2
        ),
        len(doc.tree.children),
    )
    fields: dict[str, list[tuple[str, int]]] = {}
    for node in doc.tree.children[:first_h2]:
        if node.type != "paragraph":
            continue
        for index in range(*node.map):
            match = re.fullmatch(
                r"(Status|Feature ID):\s*(.*?)\s*", doc.lines[index]
            )
            if match:
                fields.setdefault(match[1], []).append((match[2], index + 1))
    return fields


def has_content(nodes: list[SyntaxTreeNode]) -> bool:
    return any(node.type != "heading" and text(node).strip() for node in nodes)


def markers(
    doc: Document, nodes: list[SyntaxTreeNode], name: str
) -> list[tuple[SyntaxTreeNode, int]]:
    result = []
    for node in nodes:
        if node.type != "paragraph":
            continue
        for index in range(*node.map):
            if doc.lines[index].lstrip().startswith(f"{name}:"):
                result.append((node, index + 1))
    return result


def check_stories(
    doc: Document, part: Section, findings: list[Finding], status: str
) -> int:
    stories: list[tuple[SyntaxTreeNode, list[SyntaxTreeNode]]] = []
    for node in part.nodes:
        if node.type == "heading" and depth(node) == 3:
            stories.append((node, []))
        elif stories:
            stories[-1][1].append(node)
    seen: set[str] = set()
    numbers: list[int] = []
    for heading, nodes in stories:
        title = text(heading)
        match = STORY_ID.match(title)
        if not match:
            add(findings, "FB011", doc.path, line(heading), f"Invalid story heading '{title}'")
            continue
        story_id = f"S{match[1]}"
        numbers.append(int(match[1]))
        if story_id in seen:
            add(findings, "FB006", doc.path, line(heading), f"Duplicate story ID {story_id}")
        seen.add(story_id)
        statements = markers(doc, nodes, "Story")
        acceptances = markers(doc, nodes, "Acceptance")
        if len(statements) > 1:
            add(
                findings, "FB008", doc.path, statements[1][1],
                f"Story {story_id} has more than one Story: statement",
            )
        if not statements or not text(statements[0][0]).removeprefix("Story:").strip():
            complete(
                findings, status, "FB008", doc.path, line(heading),
                f"Story {story_id} has no Story: statement",
            )
        if len(acceptances) > 1:
            add(
                findings, "FB009", doc.path, acceptances[1][1],
                f"Story {story_id} has more than one Acceptance: block",
            )
        if not acceptances:
            complete(
                findings, status, "FB009", doc.path, line(heading),
                f"Story {story_id} has no Acceptance: block",
            )
        else:
            marker, at = acceptances[0]
            position = nodes.index(marker)
            next_node = nodes[position + 1] if position + 1 < len(nodes) else None
            criteria = (
                sum(
                    has_content(item.children)
                    for item in next_node.children
                    if item.type == "list_item"
                )
                if next_node and next_node.type in {"bullet_list", "ordered_list"}
                else 0
            )
            if not criteria:
                complete(
                    findings, status, "FB010", doc.path, at,
                    f"Story {story_id} has no acceptance criteria",
                )
    if any(number != index + 1 for index, number in enumerate(numbers)):
        complete(
            findings, status, "FB007", doc.path,
            line(stories[0][0]) if stories else line(part.heading),
            "Story IDs must be sequential from S1",
        )
    return len(stories)


def brief_directory_id(path: str) -> str | None:
    parts = path.split("/")
    if (
        len(parts) == 4
        and parts[:2] == [".workflow", "features"]
        and parts[3] == "brief.md"
        and FEATURE_ID.fullmatch(parts[2])
    ):
        return parts[2]
    return None


def check_brief(doc: Document, findings: list[Finding]) -> tuple[str | None, int]:
    directory_id = brief_directory_id(doc.path)
    if directory_id is None:
        add(
            findings, "FB017", doc.path, 1,
            "Feature Brief must be at .workflow/features/B-xxxx/brief.md",
        )
    headings = [node for node in doc.tree.children if node.type == "heading"]
    h1 = [node for node in headings if depth(node) == 1]
    if len(h1) != 1 or not text(h1[0]).strip():
        add(
            findings, "FB001", doc.path, line(h1[1]) if len(h1) > 1 else 1,
            "Feature Brief must have exactly one nonempty H1",
        )
    elif headings[0] is not h1[0]:
        add(
            findings, "FB001", doc.path, line(h1[0]),
            "The first heading in a Feature Brief must be its H1",
        )
    fields = preamble_fields(doc)
    statuses = fields.get("Status", [])
    ids = fields.get("Feature ID", [])
    if len(statuses) != 1 or statuses[0][0] not in STATUSES:
        add(
            findings, "FB002", doc.path,
            statuses[1][1] if len(statuses) > 1 else statuses[0][1] if statuses else 1,
            "Status must occur once and be one of: " + ", ".join(STATUSES),
        )
    status = statuses[0][0] if statuses and statuses[0][0] in STATUSES else "Draft"
    if len(ids) != 1 or not FEATURE_ID.fullmatch(ids[0][0]):
        add(
            findings, "FB003", doc.path,
            ids[1][1] if len(ids) > 1 else ids[0][1] if ids else 1,
            "Feature ID must occur once and have form B-xxxx",
        )
    elif directory_id is not None and directory_id != ids[0][0]:
        add(
            findings, "FB003", doc.path, ids[0][1],
            f"Feature ID {ids[0][0]} does not match directory {directory_id}",
        )
    parts_by_name: dict[str, Section] = {}
    for part in sections(doc):
        if part.name not in NAMED_SECTIONS:
            continue
        if part.name in parts_by_name:
            add(
                findings, "FB004", doc.path, line(part.heading),
                f"Duplicate section '{part.name}'",
            )
        else:
            parts_by_name[part.name] = part
    for name in REQUIRED:
        part = parts_by_name.get(name)
        if part is None:
            complete(findings, status, "FB004", doc.path, 1, f"Missing section '{name}'")
        elif name != "Stories and acceptance" and not has_content(part.nodes):
            complete(
                findings, status, "FB005", doc.path, line(part.heading),
                f"Section '{name}' is empty",
            )
    for name in NAMED_SECTIONS - set(REQUIRED):
        part = parts_by_name.get(name)
        if part and not has_content(part.nodes):
            complete(
                findings, status, "FB005", doc.path, line(part.heading),
                f"Section '{name}' is empty",
            )
    story_part = parts_by_name.get("Stories and acceptance")
    if story_part and not check_stories(doc, story_part, findings, status):
        complete(
            findings, status, "FB005", doc.path, line(story_part.heading),
            "Stories and acceptance has no stories",
        )
    check_size(doc, findings, LIMITS["feature_brief"], "Feature Brief")
    return (ids[0][0] if ids else None, ids[0][1] if ids else 1)


def links_in(node: SyntaxTreeNode, at: int = 1) -> list[tuple[str, int]]:
    if node.map:
        at = line(node)
    links = []
    if node.type == "link":
        links.append((node.attrs["href"], at))
    if node.type == "image":
        links.append((node.attrs["src"], at))
    for child in node.children:
        links.extend(links_in(child, at))
    return links


def local_target(source: Path, url: str) -> tuple[Path, str] | None:
    try:
        target = urlsplit(url)
        if target.scheme or target.netloc or url.startswith("//"):
            return None
        path = (source.parent / unquote(target.path)).resolve()
    except (ValueError, OSError):
        return None
    if not target.path:
        path = source
    return path, unquote(target.fragment)


def check_backlog(
    backlog: Document | None,
    briefs: list[tuple[Document, str | None, int]],
    findings: list[Finding],
) -> None:
    items: dict[str, Section] = {}
    backlink_counts: dict[str, int] = {}
    if backlog:
        check_size(backlog, findings, LIMITS["backlog"], "Backlog")
        check_records(backlog, findings, LIMITS["backlog_item"], "Backlog item")
        for part in sections(backlog):
            match = BACKLOG_ID.match(part.name)
            if not match:
                continue
            identity = match[1]
            if identity in items:
                add(
                    findings, "FB014", backlog.path, line(part.heading),
                    f"Duplicate backlog ID {identity}",
                )
            else:
                items[identity] = part
        for identity, part in items.items():
            canonical = (backlog.file.parent / "features" / identity / "brief.md").resolve()
            matching = [
                at
                for node in part.nodes
                for url, at in links_in(node)
                if (target := local_target(backlog.file, url)) and target[0] == canonical
            ]
            backlink_counts[identity] = len(matching)
            if len(matching) > 1:
                add(
                    findings, "FB013", backlog.path, matching[1],
                    f"Backlog item {identity} links to features/{identity}/brief.md more than once",
                )
    seen_ids: dict[str, str] = {}
    for doc, identity, id_line in briefs:
        if identity in seen_ids:
            add(
                findings, "FB016", doc.path, id_line,
                f"Feature ID {identity} also occurs in {seen_ids[identity]}",
            )
        elif identity:
            seen_ids[identity] = doc.path
        directory_id = brief_directory_id(doc.path)
        if directory_id is None:
            continue
        item = items.get(directory_id)
        if item is None:
            add(findings, "FB012", doc.path, 1, f"No backlog item for {directory_id}")
        elif not backlink_counts.get(directory_id):
            add(
                findings, "FB013", backlog.path, line(item.heading),
                f"Backlog item {directory_id} has no link to features/{directory_id}/brief.md",
            )


def check_other_sizes(docs: list[Document], findings: list[Finding]) -> None:
    for doc in docs:
        path = doc.path
        if path == ".workflow/backlog.md" or path.endswith("/brief.md"):
            continue
        if path == ".workflow/direction.md":
            check_size(doc, findings, LIMITS["direction"], "Direction")
        elif re.fullmatch(r"\.workflow/direction/[^/]+\.md", path):
            check_size(doc, findings, LIMITS["direction_topic"], "Direction topic")
        elif path == ".workflow/context.md":
            check_size(doc, findings, LIMITS["context"], "Context")
            check_records(doc, findings, LIMITS["context_entry"], "Context entry")
        elif re.fullmatch(r"\.workflow/decisions/pdr/[^/]+\.md", path):
            check_size(doc, findings, LIMITS["pdr"], "PDR")
        elif re.fullmatch(r"\.workflow/decisions/adr/[^/]+\.md", path):
            check_size(doc, findings, LIMITS["adr"], "ADR")
        elif re.fullmatch(r"\.workflow/features/[^/]+/acceptance-[^/]+\.md", path):
            check_size(doc, findings, LIMITS["acceptance_report"], "Acceptance Report")


def check_markdown(
    root: Path, docs: list[Document], findings: list[Finding]
) -> None:
    cache = {doc.file: doc for doc in docs}
    for doc in docs:
        previous_depth = 0
        for node in doc.tree.children:
            if node.type == "heading":
                level = depth(node)
                if level > previous_depth + 1:
                    add(
                        findings, "MD001", doc.path, line(node),
                        "Heading level skips an intermediate level",
                    )
                previous_depth = level
        for node in doc.tree.children:
            for url, at in links_in(node):
                if url == "":
                    add(findings, "MD001", doc.path, at, "Link has an empty URL")
                    continue
                target = local_target(doc.file, url)
                if target is None:
                    continue
                path, anchor = target
                if not path.is_file():
                    add(findings, "LINK001", doc.path, at, f"Cannot find file `{url}`")
                    continue
                if anchor and path.suffix.lower() in {".md", ".markdown"}:
                    if path not in cache:
                        cache[path] = parse(root, path)
                    anchors = {
                        heading.attrs.get("id")
                        for heading in cache[path].tree.children
                        if heading.type == "heading"
                    }
                    if anchor not in anchors:
                        add(
                            findings, "LINK002", doc.path, at,
                            f"Anchor {url} does not exist",
                        )


def check(root: Path) -> list[Finding]:
    root = root.resolve()
    workflow = root / ".workflow"
    docs = sorted(
        (parse(root, path) for path in workflow.rglob("*.md")) if workflow.exists() else [],
        key=lambda doc: doc.path,
    )
    findings: list[Finding] = []
    backlog = next((doc for doc in docs if doc.path == ".workflow/backlog.md"), None)
    briefs = [
        (doc, *check_brief(doc, findings))
        for doc in docs
        if doc.path.endswith("/brief.md")
    ]
    check_backlog(backlog, briefs, findings)
    check_other_sizes(docs, findings)
    check_markdown(root, docs, findings)
    return sorted(findings, key=lambda item: (item.path, item.line, item.code, item.message))


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    try:
        findings = check(root)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Workflow validation failed: {error}", file=sys.stderr)
        return 2
    for finding in findings:
        severity = " warning" if finding.warning else ""
        print(f"{finding.code}{severity} {finding.path}:{finding.line}\n{finding.message}")
    if not findings:
        print("Workflow documents passed validation.")
    return 1 if any(not finding.warning for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
