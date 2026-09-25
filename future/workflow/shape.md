# Shape

Status: Draft

## Purpose

Shape turns broad Direction ideas and Backlog items into small, coherent
features. It establishes what behaviour should exist, who benefits, where the
feature's boundaries lie, and how later Acceptance can recognize success.

Every feature passes through Shape. Straightforward features may need only a
short discussion. Broad ideas may require several Shape sessions and may split
into several related features.

Shape does not decide how a feature will be implemented.

## Document guides

Shape uses the project [Direction](../documents/direction.md) and
[Backlog](../documents/backlog.md), creates and maintains
[Feature Briefs](../documents/feature-brief.md), and may update
[Context](../documents/context.md), create a
[PDR](../documents/pdr.md), or create an [ADR](../documents/adr.md) within the
boundaries described below.

## Responsibilities

Shape:

- translating broad Direction ideas into candidate features;
- refining, splitting, combining, or replacing Backlog items;
- finding the smallest coherent features that deliver observable value;
- maintaining every Feature Brief touched during the discussion;
- defining user or system stories, expected behaviour, scope, and non-goals;
- deriving observable acceptance criteria from stories and constraints;
- exposing assumptions, ambiguity, failure cases, and boundary conditions;
- investigating repository reality and prior art when they may change the
  desired behaviour;
- recording durable product decisions and shared constraints in their canonical
  documents;
- deciding with the user when a Feature Brief is ready for Design; and
- selecting at most one ready feature as the next Design input.

Shape is not responsible for:

- internal APIs, module boundaries, data structures, or implementation plans;
- selecting libraries or frameworks;
- writing implementation code or executable contracts;
- designing tests around internal structure;
- implementing several related features as one delivery; or
- treating tentative discussion as an accepted requirement.

## Inputs

Shape reads only the context relevant to the work:

| Input | Use in Shape |
| --- | --- |
| Direction | Explains the intended end state and supplies broad ideas. |
| Backlog | Supplies candidate work and records relationships between future features. |
| Draft Feature Briefs | Preserve the current understanding and unresolved questions for substantial features. |
| Ready Feature Briefs | Expose neighbouring behaviour and boundaries that new work must respect. |
| Durable decisions and shared constraints | Constrain behaviour already settled elsewhere. |
| Repository state | Shows what the system currently does and tests assumptions about existing behaviour. |
| User discussion | Supplies goals, judgement, corrections, and explicit readiness agreement. |

Direction and Backlog entries are not requirements. Shape must not silently
promote their wording into accepted feature behaviour.

## Artifacts and authority

| Artifact | Meaning during Shape | Authority |
| --- | --- | --- |
| Backlog item | Compact description of possible work and its relationships. | Not accepted behaviour. |
| Draft Feature Brief | Durable working description of a feature. It may contain open questions and tentative boundaries. | Not accepted behaviour. |
| Ready Feature Brief | Agreed feature behaviour, boundaries, stories, and acceptance criteria. | Authoritative input to Design. |
| Shared decision or constraint document | Behaviour or reasoning that applies beyond one feature. | Authoritative within its stated scope. |
| Conversation | Exploration, questions, alternatives, and temporary reasoning. | Disposable. |

Shape does not maintain a separate Shape Context. Draft Feature Briefs are its
normal persistent working memory. Stable relationships between future work
belong in the Backlog. Conversation is disposable. Do not create separate Shape
notes, context dumps, or handoff documents.

## Feature Brief lifecycle

```text
Backlog item
    ↓ enough understanding to need a durable working document
Draft Feature Brief
    ↓ explicit Shape agreement
Ready Feature Brief
    ↓ selected as the next feature
Design
```

A Feature Brief may exist long before it is ready. Shape updates every touched
brief throughout the discussion so important knowledge does not depend on model
memory or chat history.

Update the affected brief when a behaviour, boundary, or important question
becomes clear enough to preserve. Make the edit before moving to another
consequential issue. Do not edit after every exploratory turn or defer all
updates until the end. Keep partial understanding in Draft and mark tentative
parts clearly.

A draft records the current best understanding rather than a chronological
transcript. It must distinguish tentative material, open questions, and
unverified assumptions from settled content.

Only explicit readiness agreement changes a draft into an authoritative Design
input. The presence of a file, detailed prose, or complete-looking sections
does not imply readiness.
Record that agreement as `Status: Ready` in the Feature Brief. Keep
`Status: Draft` until the agreement occurs. If later evidence requires a
material change to behaviour, scope, stories, or acceptance criteria, return
the brief to Shape and set `Status: Draft` before changing that contract.

## Operating model

Shape is a collaborative discussion between the user and Mike. Build a current
understanding of each feature, expose inconsistencies and hidden assumptions,
and revise that understanding as the discussion progresses. Keep one
consequential issue active. Explore tightly coupled questions together when
separating them hides a trade-off. Do not walk through behaviour categories as
a questionnaire.

Reason before asking for the next product judgment. Investigate when evidence
can settle a question. State supported factual conclusions clearly. Synthesize
what is settled and name the remaining judgment before asking. Do not give the
user options, suggestions, or recommendations. Ask an open question that helps
the user work out the desired behaviour.

Before raising an objection, test it: "If this feature ships as currently
described, Y happens because Z." Y is a concrete consequence. Z is the
mechanism, supported by repository evidence, external evidence, or a specific
unresolved choice. If either part cannot be named, drop the objection.
Investigate an important unknown or keep it as an open question instead of
calling it a defect. State what is verified, inferred, and still unknown. Name
the evidence that could change the assessment. Investigate checkable
uncertainty before asking the user to decide a product question.

Discuss one consequential issue until it is understood, resolved, or safely
deferred. A question, objection, or counterexample from the user continues that
issue; it does not close it. Challenge weak reasoning and inconsistencies with
evidence, then let the user make the product judgment. Record material open
questions in the Draft Feature Brief.

The activities below can recur as understanding changes. Their order is not a
question sequence.

### 1. Orient

Read the main Direction sections and linked topic documents that motivate the
work, selected Backlog items, existing Feature Briefs, durable decisions, and
current repository behaviour.
Load deeper research only when it can affect the active question.

### 2. Establish the shaping scope

Identify the broad idea or related Backlog items being discussed. Decide whether
the work concerns one candidate or a small related group whose boundaries,
ordering, or behaviour must be understood together.

Shape together only features that need joint reasoning. Once a candidate can be
shaped independently without creating inconsistent boundaries, leave it for a
later Shape round.

### 3. Create or update Feature Briefs

Keep a compact idea in the Backlog while that is sufficient. Create a draft
Feature Brief when the feature needs durable stories, behavioural detail, open
questions, or boundaries that do not belong in a Backlog entry.

Update each affected brief as understanding changes. Remove superseded wording
instead of accumulating a conversation log.

### 4. Explore behaviour

Use stories and concrete scenarios to examine:

- actors and intended value;
- successful behaviour;
- relevant failure and boundary behaviour;
- permissions and externally visible safety boundaries;
- persistence and lifecycle where users or systems can observe them;
- compatibility with existing behaviour;
- explicit scope and non-goals;
- relationships with neighbouring features; and
- assumptions that could materially change the feature.

Inspect the repository before relying on claims about existing behaviour.
Investigate prior art when it may reveal missing use cases, established
expectations, or a simpler boundary.

### 5. Converge

Prefer the smallest vertical slice that provides user or system value. A layer,
component, schema, endpoint, or abstraction without independent value is an
engineering task rather than a feature.

Resolve, verify, remove, or explicitly defer consequential assumptions. Keep a
brief in draft while an unresolved issue could materially change its behaviour
or boundaries.

### 6. Establish readiness

Review each candidate brief against its stories, acceptance coverage, scope,
non-goals, assumptions, and neighbouring features. Present remaining concerns
to the user rather than silently choosing an answer.

The user and Mike explicitly agree when a brief is ready. Shape may make several
related briefs ready in one round when joint shaping was necessary.

### 7. Update the Backlog and select the next feature

Record the resulting feature boundaries, readiness, and stable relationships in
the Backlog. Ready briefs that are not selected remain available for later work.

Select no more than one ready Feature Brief for Design. Design never receives a
group of features.

## Stories and acceptance criteria

Every feature has at least one durable user or system story that expresses an
independently observable outcome. Do not invent an actor or a system story to
satisfy the document structure. If the work has no independent observable
outcome, classify it as engineering work that supports another feature.

A story identifies:

- an actor;
- a relevant situation;
- an intent or action; and
- an observable result.

Stories do not require rigid "As a user" wording.

Acceptance criteria make stories verifiable:

- every story has acceptance coverage;
- every criterion traces to a story or a named feature-wide constraint;
- criteria describe observable behaviour rather than implementation details;
- criteria cover relevant failures and boundaries, not only successful use; and
- criteria do not prescribe test code or internal structure.

Keep criteria that span stories within one feature in that Feature Brief's
feature-wide acceptance section. Put behaviour or constraints shared by several
features in one canonical document, and link every affected Feature Brief to
that document. Do not rely on agents to rediscover an unlinked shared rule.

Implementation creates tests and other evidence for the criteria. The later
Acceptance phase independently evaluates that evidence and the delivered
system.

## Outputs

A Shape session may produce any combination of:

- clarified, split, added, or replaced Backlog items;
- updated draft Feature Briefs;
- one or more ready Feature Briefs;
- durable product decisions or shared constraint documents;
- links between affected Feature Briefs and shared documents; and
- one ready Feature Brief selected for Design.

A useful session may end after Backlog or draft refinement. That is progress,
but it does not complete Shape or trigger Design.

## Completion and transition

Shape is complete for a feature when:

- the feature is a small, coherent vertical slice;
- at least one story demonstrates its value;
- agreed behaviour and important boundaries are clear;
- scope and non-goals are intentional;
- every story has observable acceptance coverage;
- every criterion traces to a story or named constraint;
- material assumptions are resolved, verified, or explicitly deferred without
  making the feature ambiguous;
- shared decisions and constraints are recorded and linked;
- no open question can materially change the feature;
- the brief is internally consistent; and
- the user and Mike explicitly agree that it is ready.

Transition to Design additionally requires exactly one ready Feature Brief to be
selected. Shape may complete several related briefs while transitioning only
one of them.

Until the workflow controller can clear context, use a manual transition. Save
and check the durable documents, then state the selected feature ID, Ready
brief, and completed checks. If Shape left repository changes, tell the user to
commit them before Design. Then tell the user to run `/clear` and start Design
for that feature. Do not continue Design in the Shape context. The new Design
context checks its repository entry gate before work starts.

## Failure and interruption behaviour

Shape remains active or leaves a brief in draft when:

- required behaviour is ambiguous;
- stories do not demonstrate coherent value;
- acceptance coverage is incomplete;
- the scope contains separable features that still need decomposition;
- repository evidence contradicts an important premise;
- related briefs or durable decisions conflict;
- a consequential product decision remains unresolved; or
- the user has not agreed that the feature is ready.

Do not hide uncertainty behind polished prose. Do not send a draft to Design to
resolve a product question. If evidence challenges Direction or an existing
durable decision, surface that conflict through the workflow that owns it.

Shape does not grant additional tool or mutation authority. External research,
remote consultation, and repository changes remain subject to the permissions
available for the active session.

## Open questions

The workflow still needs to define:

- the Backlog item lifecycle beyond understanding maturity;
- whether readiness requires an independent cold review for every feature.
