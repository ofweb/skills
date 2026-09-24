---
name: direction
description: Discuss and maintain a project's intended end state. Use for broad project ideas, tensions, or learning that may change Direction or the Backlog, before feature shaping.
---

# Direction

Use Direction to develop one cohesive view of what the project should become.
The user decides consequential changes to that view. Direction remains open as
the project learns. A session can end after its durable results are saved.

## Orient

Read `.workflow/direction.md` and the related parts of `.workflow/backlog.md`.
Follow links to decisions, definitions, research, Feature Briefs, or code only
when they can affect the current question. If either canonical file is absent,
check for an existing copy elsewhere. Do not create a second copy or migrate it
within this skill. Tell the user when a separate migration is needed.

## Discuss

Identify how the idea or evidence relates to the intended end state. Make the
important uncertainty concrete before turning it into possible work. Examine
the goal, affected people or systems, long-term effects, assumptions, and
tensions with existing Direction. Check repository or external evidence when it
can settle a premise.

Work with the user through one consequential question or tension at a time.
Contribute evidence and challenge assumptions. Do not lead with a recommendation
or an option menu. Do not promote an idea or research result into Direction
without the user's judgment. Keep genuine uncertainty visible.

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

Use `direction-document` for every Direction document change. Use
`backlog-document` for every Backlog change, including small edits. Use the
matching document skill for a PDR or Context entry when that skill is available.
If it is unavailable, identify the result that still needs its canonical
record. Do not hide it in another document or claim that persistence is complete.

Rewrite affected Direction sections to show current understanding. Remove
superseded text. Link related records instead of copying them. After delivered
work, change Direction only when the intended end state changes. Confirming
existing understanding needs no document edit.

End a session when its useful results have a canonical home and important open
questions remain visible. A session boundary does not mark Direction complete.
