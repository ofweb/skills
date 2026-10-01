---
name: backlog-document
description: Record agreed future features and their readiness for Shape in the shared Backlog at .workflow/backlog.md.
---

# Backlog

The Backlog retains feature-level future work that the user and model agree is
worth doing. Each item has a path toward Shape and an observable outcome.
The file at `.workflow/backlog.md` is authoritative about retained work and
durable relationships, not accepted feature behaviour or work order.

Create the file with `# Backlog` during initial Direction setup, even when no
items exist yet.

If the canonical file is absent, check for an existing Backlog elsewhere. Do
not create a duplicate or migrate an existing file in this skill. Present the
found path and required canonical destination. Recommend a separate migration
to keep one authoritative Backlog. Ask the user to approve starting that
migration or request changes. Keep this file operation blocked until the
migration is complete.

## Item format

Use one section per item. Assign a stable `B-0001` style ID with the next unused
number. Keep the ID when the title or status changes.

```markdown
# Backlog

## B-0001: Concise title

- Status: Needs Direction
- Value: Why this work is worth doing.
- Direction: [Relevant topic](direction/topic.md)
- Feature Brief: Relative link, when one exists.
- Relationships: Durable dependency, order, overlap, or group, when relevant.
```

Select exactly one status. Omit an optional line when it has no value.
For `Needs Direction`, link to the Direction material that holds the unresolved
question. For `Ready for Shape`, keep the Direction link when it gives useful
context. Link a Direction topic document when it explains the item's source
more precisely than the main document. Do not copy the question into the Backlog.

When a Feature Brief exists, link `features/<item-id>/brief.md`. The item ID is
an identity, not a priority or delivery order.

Record only durable dependencies or sequence constraints. Do not record a
transient priority order or the user's active Shape selection.

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

## Ownership and content

Direction owns item creation and readiness for Shape. Add an item only after
Direction establishes why the feature exists, how it fits the intended end
state, and user agreement that it is worth retaining. Do not add items while
exploring possibilities. Shape may propose a split or new item, but Direction
decides whether to retain it and when it is Ready for Shape.

Do not use the Backlog for open Direction questions, research tasks, architecture
tasks, or internal engineering work without its own observable outcome. Keep
refactors, helper work, module changes, migrations, and implementation steps
within the owning feature's later Design or Implementation. Return a possible
separate technical capability to Direction for discussion.

Keep feature behaviour in Feature Briefs. Do not copy their requirements,
stories, acceptance criteria, implementation plans, or discussion transcripts
into an item. For a `Ready for Shape` item, use `feature-brief-document` to
create a Draft when useful behavioural understanding needs a durable home.

## Maintenance

Shape may update existing items when their agreed boundaries or relationships
change. Update affected links when an item is replaced or removed. Delete items
that are no longer plausible work, including delivered items with no remaining
work. Merge or replace duplicate items. Do not create an archive for removed
items; Git preserves history.

## Size and validation

Aim for 20–50 words per item. The hard limit is 80 words per item and 1,800
words for the whole file. Near a limit, first remove stale, duplicate, or
overly detailed items. Move feature behaviour to Feature Briefs. Remove stale
links and repeated explanations. The limits are guardrails, not size targets.

Invoke `concise-prose` before writing or revising the Backlog. Apply its
principles and run `prose-check` as described there. Install
`workflow-document-check` alongside this skill and use it after the edit.
Prune or restructure after a hard-limit failure. Check that every item has a
stable ID, one status, and a clear reason to retain the work.
