---
name: backlog-document
description: Create or revise the shared Backlog at .workflow/backlog.md when agreed future implementation work or its readiness for Shape changes.
---

# Backlog

The Backlog retains future implementation work that the user and model agree is
worth doing. Direction and Shape maintain one file at `.workflow/backlog.md`.
It is authoritative about retained work and durable relationships, not accepted
feature behaviour or work order.
Create the file with `# Backlog` during initial Direction setup, even when no
items exist yet.

If the canonical file is absent, check for an existing Backlog elsewhere. Do
not create a duplicate or migrate an existing file in this skill. Ask for a
separate migration.

## Item format

Use one section per item. Assign a stable `B-0001` style ID with the next unused
number. Keep the ID when the title or status changes.

```markdown
# Backlog

## B-0001: Concise title

- Status: Needs Direction
- Value: Why this work is worth doing.
- Open Direction: Consequential question, when one remains.
- Feature Brief: Relative link, when one exists.
- Relationships: Durable dependency, order, overlap, or group, when relevant.
- Source: Link to Direction or a durable decision, when useful.
```

Select exactly one status. Omit an optional line when it has no value.
When a Feature Brief exists, link `features/<item-id>/brief.md`. The item ID is
an identity, not a priority or delivery order.

The status describes whether Direction is sufficiently settled for Shape:

| Status | Meaning |
| --- | --- |
| Needs Direction | We agree this work is worth doing, but consequential Direction questions remain. |
| Ready for Shape | Direction is sufficiently settled for this work to enter Shape. |

`Ready for Shape` does not commit the work to delivery or mean that Direction
is complete. New evidence can return an item to `Needs Direction`. A Feature
Brief link shows its relationship to later stages. The link does not set the
status by itself.

When an existing item uses `Unclear`, `Framed`, or `Understood`, review whether
the work still merits a Backlog item. Set its new status from its current
Direction, not from a direct marker translation.

## Maintenance

Add an item after Direction establishes why it exists and how it fits the
intended end state. Agree with the user that the work is worth retaining.
Do not add items while exploring possibilities. Do not use the Backlog for open
Direction questions, research tasks, architecture tasks, or implementation
details. An item may retain a consequential Direction question when the work
itself is already agreed. Revise items when Shape changes their boundaries.
Shape can split, combine, replace, or relate items. Keep IDs
stable for retained items. Update affected links when an item is replaced or
removed. Delete items that are no longer plausible work, including delivered
items with no remaining work. Merge or replace duplicate items. Do not create
an archive for removed items; Git preserves history.

Aim for 20–50 words per item. The hard limit is 80 words per item and 1,800
words for the whole file. Near a limit, first remove stale, duplicate, or
overly detailed items. Move feature behaviour to Feature Briefs. Remove stale
links and repeated explanations. The limits are guardrails, not size targets.

Link a relevant Direction topic document when it explains an item's source more
precisely than the main document.

Record only durable dependencies or sequence constraints. Do not record a
transient priority order or the user's active Shape selection. Do not copy
Feature Brief requirements, stories, acceptance criteria, implementation plans,
or discussion transcripts into an item. Create a draft Feature Brief when
durable behavioural detail no longer fits a compact Backlog item.

Invoke `concise-prose` before writing or revising the Backlog. Follow its STE100
and Vale repair loop until `prose-check` passes. Install
`workflow-document-check` alongside this skill and use it after the edit.
Prune or restructure after a hard-limit failure. Check that every item has a
stable ID, one status, and a clear reason to retain the work.
