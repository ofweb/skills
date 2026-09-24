# Direction document

Status: Draft

## Purpose

The Direction document gives the project one concise, cohesive intended end
state. Direction maintains it through discussion with the user as ideas enter
the project and completed work changes what is understood.

## Ownership and cardinality

- One Direction document exists per project.
- Store it at `.workflow/direction.md` from the project root.
- Direction creates and maintains it with the user.
- Shape reads it but does not silently redefine it.
- Evidence from later work may trigger a new Direction discussion.
- Direction never becomes complete; individual discussions end after their
  durable results are preserved.

## Contains

- the project's overall goal;
- the intended mature user or system experience;
- long-term capabilities and properties;
- important end-state boundaries;
- tensions between desired properties;
- unresolved questions about the intended destination; and
- links to PDRs or research needed to understand a statement.

## Does not contain

- a Backlog, roadmap, delivery order, or progress report;
- detailed feature behaviour or acceptance criteria;
- implementation architecture, technology choices, or task breakdowns;
- a catalogue of completed features;
- transient ideas that have not joined the cohesive direction; or
- copied rationale already owned by a PDR.

## Authority and maintenance

The document is authoritative about the intended destination, not about current
feature requirements or implementation. Direction revises it when the user's
understanding of that destination changes, not whenever work finishes.

Explicit questions and tensions may remain while Direction is unresolved. Their
presence does not make the rest of the document non-authoritative, provided the
uncertainty is clearly bounded.

Keep it short enough to orient a fresh context before selecting deeper material.
Move candidate work to the Backlog and durable product reasoning to PDRs.

Aim for 300–500 words. The hard limit is 800 words. Near that limit, remove
resolved questions, superseded direction, feature detail, copied PDR rationale,
and research detail before shortening the remaining meaning. Git preserves
earlier versions; this document describes the current destination.

## Relationships

Direction creates and maintains the Backlog with Shape. Backlog items should
identify the part of Direction they advance when that relationship is not
obvious. Feature Briefs may link to Direction but must state their own agreed
behaviour.
