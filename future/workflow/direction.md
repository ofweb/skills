# Direction

Status: Draft

## Purpose

Direction is the ongoing discussion that turns ideas and project learning into
one cohesive understanding of what the project should become. It maintains a
short [Direction document](../documents/direction.md) and shares stewardship of
the [Backlog](../documents/backlog.md) with Shape.

Direction is never complete. Individual sessions end, but new ideas, research,
experiments, and delivered features may change the intended end state.

## Responsibilities

Direction:

- receives and examines ideas with the user;
- maintains a unified intended end state without forcing false certainty;
- exposes tensions, contradictions, assumptions, and unanswered end-state
  questions;
- keeps the Direction document concise and internally understandable;
- creates and maintains Backlog items with Shape;
- uses delivered work and targeted experiments as evidence;
- investigates relevant prior art and adjacent solutions to test assumptions
  and expand the discussion;
- creates a [PDR](../documents/pdr.md) when durable product reasoning must
  survive the discussion;
- updates [Context](../documents/context.md) when stable project terminology is
  resolved; and
- links deeper research without copying it into the Direction document.

Direction does not:

- turn every idea into project direction or Backlog work;
- define Feature Briefs, user stories, or acceptance criteria;
- choose implementation architecture or technology;
- maintain project status, completed-work history, or a delivery plan;
- assign a persistent "next feature" or transient priority order; or
- recommend an answer or present an option menu to the user.

## Inputs

Direction may use:

- ideas and questions from the user;
- the current Direction document;
- the Backlog and existing [Feature Briefs](../documents/feature-brief.md);
- PDRs and Context definitions;
- current repository behaviour;
- focused research, experiments, and external evidence; and
- learning returned after delivered features.

Load only material that can affect the active Direction question. Do not load
the full repository or research tree merely because it exists.

## Artifacts and authority

| Artifact | Use in Direction | Authority |
| --- | --- | --- |
| Direction document | Current cohesive understanding of the intended end state, including explicit tensions and open questions. | Intended destination, not feature requirements or design |
| Backlog | Possible work and stable relationships discovered through Direction and Shape. | Inventory, not accepted behaviour or work order |
| PDR | Durable product or behavioural decision and rationale. | Decision within its stated scope |
| Context | Stable project-specific terminology. | Meaning of defined terms |
| Research | Evidence and prior art followed only when needed. | Supporting material, not policy |
| Conversation | Exploration and reasoning with the user. | Disposable after durable knowledge is preserved |

## Operating model

Direction is collaborative, question-led, and non-recommending. Mike contributes
evidence, challenges assumptions, and raises one important question or tension
at a time. The user supplies judgement and decides how the intended direction
changes.

### 1. Orient

Read the current Direction document and the Backlog areas connected to the
idea. Follow links to PDRs, Context, research, Feature Briefs, or code only when
they can change the discussion.

### 2. Establish the question

Identify how the idea or new evidence relates to the intended end state. Make
the uncertainty concrete without converting it into a feature or proposed
solution prematurely.

### 3. Investigate and discuss

Examine the goal, affected users or systems, long-term consequences, tensions
with existing direction, and assumptions required for the idea to make sense.

Ask what must be true for the idea to make sense. Verify checkable premises
against project knowledge, repository behaviour, or external evidence.

Look for existing, related, or adjacent solutions when they could reveal
alternatives, common failures, useful patterns, or simpler boundaries. Bring
the useful discoveries into the discussion and test them against the project's
goal. Do not treat external implementations as authority or produce a large
research report by default.

Direction may request deeper research, an experiment, or future feature work
when a bounded question cannot be answered in the current discussion.

Ordinary uncertainty stays inside Direction. [Decision](decision.md) remains
available when a high-impact question must formally interrupt Direction and use
an isolated context, but Direction does not invoke it merely because an open
question exists.

### 4. Route what was learned

Place each durable result in one canonical home:

- changed understanding of the intended end state → Direction document;
- possible future work or evidence-gathering work → Backlog;
- durable product or behavioural choice → PDR;
- stable terminology → Context;
- unresolved end-state question or tension → Direction document;
- detailed supporting evidence → research; and
- temporary reasoning with no future value → nowhere.

Do not duplicate the same conclusion across these documents. Link to the
canonical source when another artifact depends on it.

### 5. Restore cohesion

Rewrite affected Direction sections so they express the current understanding
rather than the history of the discussion. Keep a question or tension visible
when it remains important; cohesion does not require pretending it is resolved.

Remove superseded wording. Move delivery ideas to the Backlog and detailed
rationale to PDRs or research before the Direction document becomes long enough
to obscure the intended destination.

### 6. End the session

A Direction session may end after any useful update. Before leaving it, preserve
durable knowledge, link affected artifacts, and make unresolved questions
visible outside the conversation.

Ending a session does not mark Direction complete. The user may later start
Shape by naming the Backlog item, draft Feature Brief, or related features to
work on. That active selection belongs to workflow state, not the Direction
document or Backlog.

## Questions and tensions

The Direction document may contain unanswered questions and tensions when they
matter to the intended end state. State them precisely enough for a future
discussion to understand what remains uncertain and why it matters.

Do not use open questions as a dumping ground for every possible feature or
implementation unknown. Feature candidates belong in the Backlog. Feature
behaviour belongs in Feature Briefs. Architecture belongs in Design and ADRs.

Resolve, reframe, or remove a Direction question when later discussion or
evidence changes it.

## Learning through delivery

Some Direction questions need working software, a prototype, an experiment, or
a delivered feature before the project can know what works. Direction records
the question and creates or updates the related Backlog item. Shape determines
whether that work becomes a feature, an engineering task, or another bounded
investigation.

After delivery, examine what was learned:

- change the Direction document only when delivery changes what the project
  should ultimately become;
- update the Backlog when future work or relationships changed;
- create, revise, or remove a PDR when a durable product choice changed; and
- make no document change when the result only confirms current understanding.

Feature completion alone is not a reason to edit the Direction document.

## Outputs

A Direction session may produce any combination of:

- a revised Direction document;
- added, changed, related, or removed Backlog items;
- a new, revised, or removed PDR;
- updated Context terminology;
- focused research or an evidence-gathering Backlog item; or
- no document change when the discussion does not alter durable knowledge.

## Session boundary

A Direction session can end when:

- the current discussion has reached a useful stopping point;
- durable results are in their canonical documents;
- unresolved questions and tensions that must survive are recorded;
- affected links are current; and
- no important conclusion exists only in the conversation.

This is a persistence boundary, not a completion gate.

## Failure behaviour

- Do not manufacture a unified answer when a genuine tension remains.
- Do not silently turn an idea, assumption, or research finding into Direction.
- Do not treat earlier effort as evidence that the current direction is right.
- Do not expand the Direction document with delivery detail to avoid creating or
  updating the Backlog.
- If evidence contradicts a PDR or Direction statement, surface the conflict
  rather than choosing one silently.
- If the discussion needs facts that are unavailable, record the question and
  identify the bounded investigation needed to obtain them.

## Open questions

The workflow still needs to define:

- the Backlog item lifecycle beyond understanding maturity;
- how evidence-gathering work is represented in the Backlog;
- the progression trigger after a feature reaches Done; and
- the workflow-state representation for the user's active Shape selection.
