# Architecture decision record

Status: Draft

## Purpose

An ADR preserves a durable architectural decision and the reason it was made.
It explains choices that code alone cannot make safe for future contributors to
reinterpret.

## Ownership and cardinality

- Shape may create an ADR only when architecture must be settled to establish
  feature feasibility, observable behaviour, or boundaries.
- Design creates ADRs for durable architectural choices discovered while
  defining implementation structure.
- Implementation does not make a new architectural decision autonomously. It
  returns the issue to Design.
- Create one record per durable decision.
- Store current records in `.workflow/decisions/adr/` with a stable `ADR-0001`
  style ID and a matching `0001-short-title.md` filename.

## Create an ADR when

All of these conditions hold:

- changing the choice later has a meaningful cost;
- a future contributor could reasonably misunderstand or reverse it without
  knowing the rationale; and
- the decision resolved a real trade-off rather than recording the only
  practical option.

Routine implementation choices belong in code. Local comments may link to an
ADR when the decision creates a non-obvious constraint.

## Contains

- a concise title and status;
- the architectural question or constraint;
- the decision and why it was made;
- non-obvious consequences when useful;
- rejected alternatives only when their rejection matters later; and
- links to affected Feature Briefs, PDRs, Context terms, or code.

An ADR may be only a short paragraph when that captures the complete decision.

## Does not contain

- feature requirements or acceptance criteria;
- an implementation plan or task list;
- a broad architecture tour;
- routine API, helper, or library choices;
- copied code structure that will become stale; or
- a transcript of the design discussion.

## Authority and maintenance

An ADR is authoritative within its stated architectural scope. Affected Feature
Briefs link to it when it constrains their behaviour or feasibility.

Aim for 200–400 words. The hard limit is 700 words. Omit sections that do not
help future reasoning. Keep only applicable architectural decisions. Delete
an obsolete ADR when nothing current depends on it. Replace or revise a
changed decision so its current constraint is clear, and update affected
links. Git preserves earlier rationale; `.workflow/` is not an archive.
