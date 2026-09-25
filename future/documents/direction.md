# Direction document

Status: Draft

## Purpose

The Direction documents give the project one cohesive intended end state.
Direction maintains them through discussion with the user as ideas enter the
project and completed work changes what is understood.

## Ownership and cardinality

- One main Direction document exists at `.workflow/direction.md`.
- Optional topic documents live at `.workflow/direction/<topic>.md`.
- Direction creates and maintains the main and topic documents with the user.
- Shape reads it but does not silently redefine it.
- Evidence from later work may trigger a new Direction discussion.
- Direction never becomes complete; individual discussions end after their
  durable results are preserved.

## Main document

The main document contains:

- the project's overall goal;
- a current synthesis of every Direction topic, with links to topic documents;
- the intended mature user or system experience across topics;
- shared end-state boundaries and tensions;
- unresolved questions that affect the whole destination; and
- links to PDRs, References, or research needed to understand a statement.

Keep every current topic represented in the main document, including topics
with their own document. The main document is the authoritative synthesis of
the whole destination.

## Topic documents

Create a topic document when one coherent part of the destination needs more
room or can be understood more clearly on its own. Give each file a clear topic
and a stable name. A topic document owns the detailed end-state statements,
boundaries, tensions, and open questions for that topic. Link it from the main
document and back to the main document.

Do not copy detailed claims into the main document. Keep the main synthesis
consistent with the topic document. When Direction changes either document,
check the other and update its summary, detail, or links as needed. Rebalance
material between documents when topic boundaries change. Remove obsolete topic
documents and stale links. Git preserves earlier versions.

## Does not contain

- a Backlog, roadmap, delivery order, or progress report;
- detailed feature behaviour or acceptance criteria;
- implementation architecture, technology choices, or task breakdowns;
- a catalogue of completed features;
- transient ideas that have not joined the cohesive direction; or
- copied rationale already owned by a PDR.

## Authority and maintenance

The Direction documents are authoritative about the intended destination, not
about current feature requirements or implementation. Direction revises them
when the user's understanding changes, not whenever work finishes.

Explicit questions and tensions may remain while Direction is unresolved. Their
presence does not make the rest of the document non-authoritative, provided the
uncertainty is clearly bounded.

Keep the main document useful for a fresh context before it selects deeper
topic material.
Move candidate work to the Backlog and durable product reasoning to PDRs.

Keep the documents concise without deleting current direction to meet a normal
word target. The main document has a hard limit of 4,000 words. Each topic
document has a hard limit of 2,000 words. These limits are ceilings, not size
targets. Near a limit, remove resolved questions, superseded direction, feature
detail, copied PDR rationale, and research detail. Rebalance coherent topic
material when that improves the document set. Git preserves earlier versions.

## Relationships

Direction creates and maintains the Backlog with Shape. Backlog items should
link to the relevant Direction topic when that relationship is not obvious.
Feature Briefs may link to Direction documents but must state their own agreed
behaviour.
