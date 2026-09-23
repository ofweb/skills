---
name: concise-prose
description: Write and review concise technical prose using Vale.
---

# Concise prose

Use this skill whenever creating or substantially editing:

- Markdown documentation
- design documents
- specifications
- README files
- AGENTS.md files
- code comments and doc comments

Optimize for information density.

Prefer deleting text over rewriting it.
Do not repeat information already apparent from code, headings, examples, or nearby text.
State behavior directly.
Avoid introductory prose, summaries of the immediately preceding text, and conversational filler.

After writing or editing prose, run:

    ~/.agents/skills/concise-prose/lint <changed-files>

Fix all reported errors you introduced.

When fixing an error, make the smallest useful change.
Deleting unnecessary prose is preferred.
Do not expand the text merely to avoid a Vale rule.
