---
name: direction
description: Help a user think through vague ideas, problems, or doubts about where a project should go. Iteratively challenge assumptions and investigate prior art or adjacent solutions when learning may change Direction or Backlog.
---

# Direction

Use Direction as an iterative discussion that helps the user understand what
the project should become. A vague idea, observed problem, concern, example,
or lesson from implementation is enough to begin. Help organize incomplete
thoughts without turning them into feature requirements. The document is a
durable result of the discussion, not its goal.

## Orient

Read `.workflow/direction.md` and relevant Backlog items when they exist.
Follow related PDRs, Context entries, research, Feature Briefs, or code only
when they can affect the current question. If a canonical file is absent,
check for an existing copy elsewhere before creating it. Do not create a
duplicate or migrate a file in this skill.

On a new project, explore the idea until there is enough shared understanding
to state a useful initial intended end state. Then create
`.workflow/direction.md` through `direction-document` and initialize
`.workflow/backlog.md` through `backlog-document`, even if empty.

## Explore and refine

Find the need beneath a proposed solution and connect it to existing Direction.
Look for consequential hidden assumptions, contradictions, implied requirements,
coupled capabilities, unnecessary constraints, and trade-offs between goals.
Explain the premise or evidence behind a challenge; do not manufacture objections.
Check material assumptions against the repository or external evidence when
possible. Distinguish facts, experiments, design choices, and user judgments.

## Investigate prior art

Proactively look for existing, related, or adjacent solutions when they could
change the discussion. Include relevant products, projects, standards, patterns,
failures, and platform capabilities. Use discoveries to expose alternatives,
trade-offs, vocabulary, or an already solved problem. Bring back only findings
that matter, explain why, and state their limits. External work is evidence and
inspiration, not authority. If investigation is blocked, preserve the unknown.

## Discuss

Move between understanding, investigation, challenge, and refinement as the
user revises or rejects an idea. New evidence may change the question. Keep one
consequential topic active; explore tightly coupled questions together when
separating them hides a trade-off. Reason and investigate before asking for the
next judgment the user must make. Do not default to interrogation, generated
option menus, or recommendations. Compare distinct approaches when evidence
or prior art makes the comparison useful. State supported factual conclusions
clearly, challenge weak reasoning, and leave consequential project judgments
to the user. A better question or bounded uncertainty can be a useful stopping
point.

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

End a session when any durable results have a canonical home and important open
questions remain visible. No document change is required when the discussion
has not changed durable knowledge. A session boundary does not mark Direction
complete.
