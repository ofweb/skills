# Product decision record

Status: Draft

## Purpose

A PDR preserves a durable product or behavioural decision and the reason it was
made. It prevents later work from rediscovering or silently contradicting a
choice whose consequences extend beyond one local feature detail.

## Ownership and cardinality

- Direction and Shape may create PDRs.
- Create one record per durable decision.
- Store records in `.workflow/decisions/pdr/` with a stable `PDR-0001` style ID
  and a matching `0001-short-title.md` filename.
- Decision discussions route product outcomes to Direction or Shape; the
  Decision mechanism does not create records merely because it ran.

## Create a PDR when

- the decision affects several features or future product behaviour;
- changing it later would invalidate meaningful work or expectations; and
- future contributors need its rationale to apply or reconsider it correctly.

Feature-specific behaviour that needs no wider rationale belongs in the Feature
Brief. Small reversible choices need no record.

## Contains

- a concise title and Accepted status;
- a stable ID;
- the product question or constraint;
- the decision and why it was made;
- the scope in which it applies;
- non-obvious consequences when useful;
- assumptions or conditions for reconsideration when useful;
- rejected alternatives only when their rejection matters later; and
- links to affected Direction material, Backlog items, or Feature Briefs.

## Does not contain

- a transcript or generated option matrix;
- complete feature requirements;
- architecture or implementation design;
- speculative possibilities with no decision;
- routine scope choices local to one Feature Brief; or
- a running history of every product discussion; or
- decisions that no longer apply.

## Authority and maintenance

A PDR is authoritative within its stated scope after the user makes the
decision. Keep unresolved candidates in Direction, Backlog, or discussion.
Every Feature Brief affected by a shared product rule must link to its current
PDR.

Aim for 150–300 words. The hard limit is 500 words. Omit sections that add no
useful information. Keep `.workflow/decisions/pdr/` as the set of applicable
decisions, not a decision archive. Delete an obsolete PDR when nothing current
depends on it. Replace a changed decision and update links. If part of the old
decision remains valid, rewrite or replace it so the current record states the
current constraint. Git preserves earlier records and rationale.
