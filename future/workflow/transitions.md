# Workflow transitions and state

Status: Draft

## Purpose

Workflow transitions move responsibility into a fresh context without losing
durable knowledge. The active step determines when its work is complete. The
workflow controller validates and performs the context change.

This guide defines high-level requirements. It does not define the controller's
storage schema, commands, or user interface.

## Responsibilities

The active workflow step:

- completes its documented exit conditions;
- writes durable knowledge to its canonical documents or code;
- runs the checks required by that step;
- identifies the proposed next responsibility;
- presents a transition declaration; and
- waits for confirmation when the transition requires it.

The workflow controller:

- validates that the current step may route to the proposed next step;
- verifies required artifacts and checks where they can be checked
  deterministically;
- records minimal handoff and pause state;
- lets the current turn finish before ending its context;
- starts the next responsibility in a fresh context; and
- leaves the current context intact when validation or confirmation fails.

Neither the step nor the controller copies temporary reasoning into the next
context.

## Transition declaration

Before a context clear, Mike states:

- which workflow step is complete;
- which documents, code, tests, reports, or other durable artifacts were
  created or updated;
- which completion checks passed;
- which step should run next; and
- that continuing will clear the current context.

The declaration should be concise and link to the affected artifacts. It is a
request to change responsibility, not a conversation summary.

For example:

> Design is complete. I updated the accepted code structure and ADR-004. The
> repository compiles, and its existing tests, formatting, and lint checks
> pass. The next step is Implementation. Continuing will clear this context.

## Confirmation policy

Every transition produces a declaration. Direction, Shape, Design, Decision,
and collaborative Acceptance transitions require explicit user confirmation
before the controller clears context.

An explicit response that accepts Design may also confirm its transition when
the preceding message identifies Implementation as the next step and warns
about the context clear.

Implementation may proceed directly to Review after a valid declaration.
Review may proceed directly to Acceptance. These two transitions do not need
another user response, which preserves unattended delivery after Design.

Automatic transitions remain visible. They skip the confirmation wait, not the
declaration, validation, state recording, or context reset.

## Context boundary

Each change of workflow responsibility starts in a fresh context. The active
model does not invoke `/clear` or replace its own session. The controller ends
the session only after the current turn and transition requirements complete.

The next context reconstructs its task from repository state and minimal
controller state. It does not inherit the preceding conversation or a generated
summary of that conversation.

Until the controller is available, the user performs the context clear after
the active step completes its checks and declares the transition. The step
gives the user the next responsibility and the canonical artifact ID or path.
Before Design, the user establishes a clean working tree, including committing
agreed Shape documents. The user runs `/clear` and starts that responsibility
in a new session. The model does not invoke `/clear` or carry a conversation
summary across the boundary. The receiving step still checks its entry
requirements.

## Minimal workflow state

Controller state contains only what is needed to restore responsibility and
locate canonical artifacts. Depending on the transition, this may include:

- the active feature;
- the completed and next workflow steps;
- the transition outcome;
- relevant document, code, test, and report locations;
- the reviewed or implemented repository revision;
- an interrupted step and return point; and
- a Decision Request or other short-lived transition input.

Workflow state is not a project document, activity log, architecture tour, or
substitute for missing durable knowledge. Unfinished features may remain
discoverable through their Feature Briefs, Acceptance Reports, and Backlog
rather than copied into one handoff.

## Routes

The normal delivery path is:

```text
Shape → Design → Implement → Review → Acceptance → Done
```

Direction is ongoing steering rather than a required start for every feature.
The user selects work for Shape. Done is a feature state rather than another
workflow responsibility.

Evidence may route work backward:

- changed or ambiguous feature behaviour → Shape;
- invalid accepted architecture → Design;
- ordinary work within accepted behaviour and Design → Implementation; and
- completed implementation → Review and then Acceptance.

Acceptance records follow-up work by likely owning step. The user selects which
step to pick up, and that step determines dependencies when it reads the
report.

## Design entry gate

Before starting Design, the controller verifies a known-good repository
baseline. The working tree must have no uncommitted or untracked changes. The
complete compilation or type check, test suite, lint checks, formatting checks,
and `prose-check` must pass. Prose validation covers all eligible project text
rather than only the current change.

Do not clear the current context or start Design when this gate fails. Report
the uncommitted change or failing check and preserve the repository state for
the next action. Mike does not repair, commit, stash, or discard the problem
unless the user requests a separate skill for that work.

## Decision interruptions

Any active responsibility may request a formal
[Decision](decision.md) interruption when its threshold is met. User agreement
to enter Decision confirms the context-clearing transition.

The controller preserves the interrupted responsibility, active feature,
canonical artifacts, evidence, and intended return point. Decision may resume
that point or reroute the workflow when its outcome invalidates the saved path.

Postponing or declining Decision does not clear context. The active
responsibility continues after durable knowledge is updated where needed.

## Model boundary

Mike remains the on-device foreground model in every workflow step and fresh
context. A transition does not replace Mike with a remote model.

Each workflow step defines when remote consultation may help. The
remote-consultation skill applies call limits, capacity checks, model selection,
cooldowns, and token accounting. Remote models return evidence or analysis to
Mike; they do not own the workflow step or its transition.

## Validation and failure behaviour

- Reject a transition when the current step's completion conditions have not
  passed.
- Reject a transition when required durable knowledge has no canonical home.
- Keep the current context when required confirmation is absent or withheld.
- Keep the current context when controller validation fails.
- Do not start the next responsibility from a partial handoff.
- Do not clear context during a tool call or unfinished model turn.
- Do not treat an automatic transition as permission to skip checks.
- Report the failed requirement so the active step can complete or correct it.

## Open questions

The controller design still needs to define:

- the exact workflow-state and pause-state schemas;
- transition outcome identifiers and permitted route validation;
- the transition request and confirmation interface;
- how controller state locates unfinished work across features;
- where short-lived Review reports and Decision Requests live;
- how automatic transitions remain visible across session replacement; and
- recovery after interruption during state persistence or session startup.
