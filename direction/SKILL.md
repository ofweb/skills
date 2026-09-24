---
name: direction
description: Discuss and maintain a project's intended end state. Use for broad project ideas, tensions, or learning that may change Direction or the Backlog, before feature shaping.
---

# Direction

Use Direction to develop one cohesive view of what the project should become.
The user decides consequential changes to that view. Direction remains open as
the project learns. A session can end after its durable results are saved.

## Orient

Read `.workflow/direction.md` and relevant Backlog items when they exist.
Follow related PDRs, Context entries, research, Feature Briefs, or code only
when they can affect the current question. If a canonical file is absent,
check for an existing copy elsewhere before creating it. Do not create a
duplicate or migrate a file in this skill.

On a new project, discuss the first intended end state with the user. When
agreed, create `.workflow/direction.md` through `direction-document` and
initialize `.workflow/backlog.md` through `backlog-document`, even if empty.

## Establish the question

Identify the question behind the idea and its relation to the intended end state.
Ask what must be true for the idea to make sense. Test checkable assumptions
against project knowledge, repository behaviour, or external evidence.

## Investigate prior art

Look for existing, related, or adjacent solutions when they could improve the
discussion. Use prior art to expose alternatives, common failures, useful
patterns, and ways to avoid inventing an unnecessary solution. Research can
expand the question; it need not only verify a factual premise. Bring useful
findings into the conversation with their limits. Do not dump a research report
or treat an external implementation as authority. If investigation is blocked,
state what remains unknown rather than inventing a premise.

## Discuss

Examine the goal, affected people or systems, long-term effects, and tensions
with existing Direction. Keep one consequential topic active at a time; discuss
tightly coupled questions together when separating them would distort the
choice. Challenge assumptions without leading with a recommendation or option
menu. The user judges how Direction changes. Keep genuine uncertainty visible.

Direction does not define Feature Briefs, acceptance criteria, architecture,
technology, delivery order, or the next feature. The user starts Shape by
naming the work to discuss. Active selection belongs to workflow state.

## Preserve results

Place each durable result in one home:

- Changed understanding of the intended end state or an unresolved end-state
  question: Direction document.
- Possible feature, engineering work, or bounded investigation: Backlog.
- Durable product or behavioural decision: PDR.
- Stable project term: Context.
- Detailed supporting evidence: research material.

Use `direction-document` for each Direction change and `backlog-document` for
each Backlog change. Use `pdr-document` for a durable product decision and
`context-document` for an agreed project term. Do not hide a missing record in
another document or claim that persistence is complete.

Rewrite affected Direction sections to show current understanding. Remove
superseded text. Link related records instead of copying them. After delivered
work, change Direction only when the intended end state changes. Confirming
existing understanding needs no document edit.

End a session when its useful results have a canonical home and important open
questions remain visible. A session boundary does not mark Direction complete.
