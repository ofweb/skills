---
name: concise-prose
description: Write and review concise Markdown prose using Vale and STE100.
---

# Concise prose

Use this skill whenever creating or substantially editing:

- Markdown documentation
- design documents
- specifications
- README files
- AGENTS.md files

Optimize for information density.

For a request to write or review text in ASD-STE100 Simplified Technical English,
read [the STE100 sub-skill](ste100/SKILL.md) before drafting. Use the guidance
there for Issue 9; this skill remains the general guide for Markdown prose.

Prefer deleting text over rewriting it.
Do not repeat information already apparent from code, headings, examples, or nearby text.
State behavior directly.
Avoid introductory prose, summaries of the immediately preceding text, and conversational filler.

After writing or editing Markdown prose, run `prose-check` on each complete
edited file:

    prose-check <edited-markdown-files>

The command also accepts Markdown on standard input. It checks written text
with Vale and STE100 and skips code blocks and inline code. Install Vale and
`cmark`. Install the tested STE100 revision and its spaCy model with:

    uv tool install 'git+https://github.com/sourdough-bread/asd-ste100-checker.git@e193ecdd66b09ce81b7c611f1c841efd8ba84cc7'
    VIRTUAL_ENV="$(uv tool dir)/asd-ste100-checker" ste100 setup

Fix reported errors. Review STE100 warnings and fix those that identify a real
problem. You do not need to explain warnings you leave.

The shared software vocabulary is in `shared-terms.yaml`. Suggest a new term
only when it names a recurring technical concept that approved words cannot
name clearly. The user adds terms manually; do not add terms to clear a finding.

When fixing an error, make the smallest useful change.
Deleting unnecessary prose is preferred.
Do not expand the text merely to avoid a Vale rule.
