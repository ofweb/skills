---
name: direction-document
description: Create or revise the project's Direction document at .workflow/direction.md. Use when Direction changes the intended end state or its important open questions.
---

# Direction document

The Direction document is the project's concise, current understanding of its
intended end state. It is authoritative about the destination, not accepted
feature behaviour or implementation.

Direction creates and maintains one file at `.workflow/direction.md` with the
user. Shape may read it but must not silently redefine it. If the canonical
file is absent, check for an existing Direction document elsewhere. Do not
create a duplicate or migrate an existing file in this skill. Ask for a
separate migration.

## Content

Use this structure, with short sections and links where useful:

```markdown
# Direction

## Goal

## Intended end state

## Boundaries and tensions

## Open questions
```

State the overall goal, the mature user or system experience, long-term
capabilities, and important boundaries. Keep Goal and Intended end state in
every document. Omit Boundaries and tensions or Open questions when empty.
State unresolved end-state questions and tensions precisely. Link PDRs or
research needed to understand a statement.

Do not add a Backlog, roadmap, delivery order, progress report, feature
requirements, architecture, task list, or completed-work catalogue. Keep
transient ideas in discussion until the user adopts them as Direction. Put
possible work in the Backlog and durable product reasoning in a PDR.

## Maintenance

Create the document when the project first agrees on an intended end state.
Revise it when that understanding changes. Feature completion alone does not
require a revision. Rewrite affected sections as current understanding, not a
chronological record. Remove superseded wording. Keep a genuine unresolved
question visible without weakening statements that remain settled.

Link related Backlog items, PDRs, Context terms, or research when those links
help a fresh reader. Keep one canonical home for each conclusion.

Use `concise-prose` for writing when available. Run `prose-check` on the edited
file when available. Before finishing, check that the file is short enough to
orient a fresh context and contains no delivery detail.
