---
name: direction
description: Discuss where a project should go. Develop vague ideas with the user, challenge assumptions, and investigate prior art when it could change Direction.
---

# Direction

Use Direction as a design discussion about what the project should become.
A vague idea, observed problem, concern, example, or lesson from implementation
is enough to begin. Develop the topic with the user before turning it into
future work. Documents are durable memory of the discussion, not its goal.

## Orient

Read `.workflow/direction.md`, relevant linked topic documents, and related
Backlog items when they exist. Follow related PDRs, Context entries,
References, research, Feature Briefs, or code only when they can affect the
current question. If a canonical file is absent, check for an existing copy
elsewhere before creating it. Do not create a duplicate or migrate a file in
this skill.

After reading relevant context, begin with an observation or concrete example
from the project. Connect the topic to existing Direction, name a consequence
or tension, and give the user a developed idea to react to. Do not wait for the
user to supply the first example or design question.

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

Investigate related or adjacent solutions when a material uncertainty, useful
comparison, or relevant prior art could change the discussion. Do not search
only because related work may exist. Use discoveries to expose alternatives,
trade-offs, vocabulary, or an already solved problem. Bring back findings that
matter, explain why, and state their limits. External work is evidence and
inspiration, not authority. If investigation is blocked, preserve the unknown.

Use `references-document` to preserve sources with durable project value and
useful user links, even when their effect on Direction remains unclear. It
owns source selection, relevance notes, and unverified claims.

## Discuss

Move between understanding, investigation, challenge, and refinement as the
user revises or rejects an idea. New evidence may change the question. Keep one
consequential topic active; explore tightly coupled questions together when
separating them hides a trade-off. Develop the idea as far as available context
allows on each turn. Prefer a concrete project example when testing an abstract
question.

Explain consequences and contradictions before asking for the user's judgment.
Do not make each reply mainly another question. Do not default to interrogation,
generated option menus, or recommendations. Compare distinct approaches when
evidence or prior art makes the comparison useful. State supported factual
conclusions clearly and challenge weak reasoning. Leave consequential project
judgments to the user.

For a consequential project judgment, bring a proposed decision and a short
reason to the discussion. Ask the user to approve or change the proposal.
After the response, continue the current Direction discussion.

Direction does not define Feature Briefs, acceptance criteria, architecture,
technology, delivery order, or the next feature. The user starts Shape by
naming the work to discuss. Active selection belongs to workflow state.

## Preserve results

Keep the Direction documents current when the intended end state materially
changes or an important unresolved end-state question needs to remain visible.
Do not edit them for a slight wording change, after every exploratory turn, or
merely because work was delivered. Keep tentative ideas out of authoritative
statements.

Record other durable results in their proper homes when they arise.

Place each durable result in one home:

- Changed understanding of the intended end state or an unresolved end-state
  question: Direction documents, through `direction-document`. Keep the main
  synthesis current across topics.
- Future feature with an observable outcome that the user and model agree is
  worth retaining: Backlog, through `backlog-document`. Understand its place in
  the intended end state
  before adding it. Keep unresolved end-state questions in Direction and link
  to them from `Needs Direction` items. Do not add research, architecture, or
  internal engineering tasks as separate Backlog items.
- Durable product or behavioural decision: PDR, through `pdr-document`.
- Stable project term: Context, through `context-document`.
- External source with durable project value and its context: References,
  through `references-document`.
- Detailed supporting evidence: research material.

Use the owning document skill for each edit. Keep current understanding in
canonical documents and link related records instead of copying them.
`direction-document` owns revision, main/topic consistency, and rebalancing.
Do not hide a missing record in another document or claim that persistence
is complete.

## Session boundaries

Continue the discussion across normal turns, including turns after document
edits. Do not interrupt them with lint output, document-change reports, workflow
summaries, `/clear`, or a generated next-step prompt.

At a genuine session boundary, give durable results a canonical home and keep
important open questions visible. No document change is required when durable
knowledge has not changed. Briefly state what changed and what remains open.
Give a workflow handoff when the user finishes Direction or switches stages.
Suggest `/clear` and a copyable prompt only when a context reset is useful.

Direction has no global completion state. A Backlog item becomes Ready for Shape
when Direction is sufficiently settled for that item. Direction owns that
readiness decision.
