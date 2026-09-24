---
name: pdr-document
description: Create or update a product decision record when Direction or Shape has a durable product or behavioural choice whose rationale matters beyond one Feature Brief.
---

# Product decision record

A PDR records a product or behavioural choice and its rationale. Direction or
Shape decides when the choice needs a record. Use one PDR per durable decision
when future contributors need its reasoning to apply, challenge, or reconsider
it. A local feature requirement belongs in its Feature Brief. Architecture
belongs in an ADR. Small reversible choices need no PDR.

## Create or update

Read related PDRs and Direction, Backlog, and Feature Brief material that bears
on the decision. Check for an existing record before creating one. Store PDRs in
`.workflow/decisions/pdr/`. Give each record the next unused `PDR-0001` style
ID and name its file `0001-short-title.md`. Keep the ID and filename stable.
If the decision already has a record elsewhere, do not create a duplicate or
migrate it in this skill.

Use this compact structure. Add optional sections only when they help a future
reader understand or revisit the choice.

```markdown
# PDR-0001: Short title

Status: Proposed

## Context

## Decision

## Rationale

## Scope

## Consequences

## Assumptions and reconsideration

## Alternatives considered

## Related records
```

Select one status. Omit optional sections with no useful content.

State the question or constraint in Context. State the choice in Decision and
the reasons in Rationale. Bound its authority in Scope. Record consequences,
assumptions, and rejected alternatives only when they matter later. Link the
Direction material, Backlog items, Feature Briefs, or other records that depend
on the decision. Do not copy their content into the PDR.

Tell the owning workflow which affected Feature Briefs must link to the PDR.

`Proposed` preserves a durable candidate awaiting the user's judgment. It is
not accepted product behaviour. Use `Accepted` only after the user agrees to
the choice. When an accepted decision changes, create a replacement PDR. Mark
the old one `Superseded by PDR-NNNN` and link both records. Preserve the old
rationale; do not rewrite history. Surface conflicts with existing accepted
records rather than silently choosing one.

Do not include discussion transcripts, option matrices, full feature
requirements, implementation plans, or status tracking. Use `concise-prose`
and `prose-check` when available. Check the ID, status, scope, and links before
finishing.
