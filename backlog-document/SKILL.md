---
name: backlog-document
description: Create or revise the shared Backlog at .workflow/backlog.md. Use when Direction or Shape changes possible work, its understanding maturity, or its durable relationships.
---

# Backlog

The Backlog is the shared inventory of possible work. Direction and Shape
maintain one file at `.workflow/backlog.md`. It is authoritative about candidate
work and durable relationships, not accepted feature behaviour or work order.
Create the file with `# Backlog` during initial Direction setup, even when no
items exist yet.

If the canonical file is absent, check for an existing Backlog elsewhere. Do
not create a duplicate or migrate an existing file in this skill. Ask for a
separate migration.

## Item format

Use one section per item. Assign a stable `B-0001` style ID with the next unused
number. Keep the ID when the title or maturity changes.

```markdown
# Backlog

## B-0001: Concise title

- Maturity: Unclear
- Possible value: Short statement or question.
- Feature Brief: Relative link, when one exists.
- Relationships: Durable dependency, order, overlap, or group, when relevant.
- Source: Link to Direction or a durable decision, when useful.
```

Select exactly one maturity marker. Omit an optional line when it has no value.
When a Feature Brief exists, link `features/<item-id>/brief.md`. The item ID is
an identity, not a priority or delivery order.

The maturity marker describes how well the idea is understood:

| Marker | Meaning |
| --- | --- |
| Unclear | The possible value or problem still needs framing. |
| Framed | The value or problem is clear, but consequential questions remain. |
| Understood | Enough is known to decide how to handle the idea in Shape. |

`Understood` does not make an item a requirement or commit it to delivery. New
evidence can move an item to an earlier marker. A Feature Brief link shows its
relationship to later stages. The link must not change the maturity marker by
itself.

## Maintenance

Add or revise compact items when Direction finds possible work or Shape changes
its boundaries. Shape can split, combine, replace, or relate items. Keep IDs
stable for retained items. Update affected links when an item is replaced or
removed. Delete items that are no longer plausible work, including delivered
items with no remaining work. Merge or replace duplicate items. Do not create
an archive for removed items; Git preserves history.

Aim for 20–50 words per item. The hard limit is 80 words per item and 1,800
words for the whole file. Near a limit, first remove stale, duplicate, or
overly detailed items. Move feature behaviour to Feature Briefs. Remove stale
links and repeated explanations. The limits are guardrails, not size targets.

Record only durable dependencies or sequence constraints. Do not record a
transient priority order or the user's active Shape selection. Do not copy
Feature Brief requirements, stories, acceptance criteria, implementation plans,
or discussion transcripts into an item. Create a draft Feature Brief when
durable behavioural detail no longer fits a compact Backlog item.

Use `concise-prose` for writing when available. Run `prose-check` on the edited
file when available. Run `python scripts/check_workflow_docs.py <project-root>`
from this skills repository.
Prune or restructure after a hard-limit failure. Check that every item has a
stable ID, one maturity marker, and a recognizable value or problem.
