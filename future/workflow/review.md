# Review

Status: Draft

## Purpose

Review evaluates one completed implementation from a fresh context. It asks
whether the feature implements the agreed behaviour and whether the change
made the system harder to understand or change.

Review uses one specialized sub-agent for each review lens. It assembles their
candidate findings into one temporary report for Acceptance.

## Responsibilities

Review:

- reconstructs the feature from durable repository state;
- examines the current change and its effects beyond the changed files;
- runs every baseline lens through a specialized sub-agent;
- invokes additional specialists when the feature exposes their concerns;
- requires exact evidence and a preliminary impact and severity for each
  candidate finding;
- keeps findings about behaviour, tests, code, comments, and structure
  separate enough to preserve their meaning;
- curates overlapping or unsupported candidates into one report;
- reports problems without recommending or implementing solutions; and
- hands the report to Acceptance in a fresh context.

Review does not:

- modify production code, tests, documents, or accepted contracts;
- suggest fixes or preferred responses;
- treat a specialist's judgement as a verified defect;
- review unrelated repository health;
- ask the user to resolve candidate findings; or
- decide that the feature is accepted.

## Inputs

Review reads:

- the ready [Feature Brief](../documents/feature-brief.md), including stories
  and acceptance criteria;
- the accepted Design expressed in code;
- linked [Direction](../documents/direction.md),
  [Context](../documents/context.md), [PDR](../documents/pdr.md), and
  [ADR](../documents/adr.md) material;
- the completed implementation and its change boundary;
- the tests and mechanical results produced by Implementation;
- relevant callers, callees, types, data flows, and neighbouring code; and
- the project's style guide, when one exists.

Review does not inherit the Implementation conversation or the implementer's
explanation of why the solution is correct.

## Output

Review produces one temporary report. It contains:

- the reviewed feature and implementation revision;
- the change-centered scope and any affected code inspected outside it;
- the specialist lenses that ran or were inapplicable;
- each retained candidate finding;
- the specialist's preliminary impact and severity; and
- any failed or incomplete review coverage.

Each candidate finding identifies:

- the lens that found it;
- the affected location;
- what was expected and observed;
- the supporting code, test, contract, story, criterion, or style-guide
  evidence; and
- the plausible consequence.

The report contains no recommendations, suggested solutions, or edits. Its
findings remain candidates until Acceptance evaluates and verifies them.

Acceptance deletes the Review report after transferring relevant results into
an [Acceptance Report](../documents/acceptance-report.md).

## Scope

Every specialist focuses on the current feature and implementation. It may
follow callers, callees, types, data flow, state, and integration boundaries
through the rest of the repository when the current change can affect them.

This impact tracing does not authorize a project-wide audit. A problem with no
causal or behavioural connection to the feature is outside Review.

## Specialist reviews

Each lens runs in its own specialized sub-agent. A specialist returns
candidate findings with evidence and a preliminary impact and severity. It
does not modify the repository or propose a response.

### Feature compliance

Check the implementation against every user story and acceptance criterion.
Identify missing behaviour, changed behaviour, and extra behaviour introduced
outside the accepted feature.

### Test coverage and effectiveness

Check whether tests protect the feature's user stories, acceptance criteria,
critical edge cases, failures, and integration paths. Every important test
should identify the regression that would make it fail.

Inspect existing tests affected by the feature for assertions, fixtures,
mocks, assumptions, and disabled cases that encode behaviour the feature has
superseded. Passing tests may still be outdated when they no longer represent
the intended system.

Do not treat test count or line coverage as evidence of behavioural coverage.

### Correctness, errors, and edge cases

Inspect algorithms, conditions, state transitions, boundary cases, cleanup,
error propagation, and failure behaviour. Compare sibling paths when one may
have omitted processing required elsewhere.

### Integration and contracts

Trace the changed code through its callers and callees. Check signatures, data
shapes, effects, error contracts, protocols, and neighbouring implementations
for drift or incompatibility.

### Structural and architectural impact

Look for unclear ownership, responsibility drift, unexpected coupling,
confused dependency direction, tangled logic and effects, hidden lifecycle or
temporal coupling, duplicate concepts, semantic duplication, unnecessary
abstraction, and increased context needed to understand the feature.

This review identifies structural damage. It does not design a refactor.

### Comments

Run a dedicated comment-review skill over comments added or changed by the
feature. Inspect nearby code and durable documents only when needed to verify
those comments.

Check that each changed comment is accurate, concise, durable, and useful.
Inline comments should preserve non-obvious intent rather than restate code.
Public API documentation may describe the contract. References must point to
stable repository knowledge and explain why it matters locally.

### Project style

When a project style guide exists, check the change against its explicit rules
and cite the rule behind every candidate finding. Skip this review when no
style guide exists. Never substitute reviewer preference for a missing rule.

Formatting and lint failures belong to mechanical checks rather than this
review.

### Type safety

Check for unchecked casts, nullability mistakes, unsafe escape hatches,
unvalidated boundary values, weakened compiler guarantees, and values used
before their invariants are established.

### Type design

Check whether changed types preserve domain distinctions and invariants, use
canonical representations, assign ownership clearly, and make invalid states
unrepresentable where practical. Report type structures that permit
contradictory fields, flags, or lifecycle states.

### Parse, do not validate

Check that raw input is parsed once at a boundary into a type that carries its
established invariant. Invalid input must not continue through the system in a
weak representation, and downstream code should not repeat validation that a
refined type could preserve.

Check constructors and deserializers for paths that bypass the invariant.
Validation failure must remain explicit at the boundary.

### Conditional specialists

Run separate security, concurrency and state, persistence and lifecycle, and
compatibility reviews when the current feature exposes those surfaces. Each
specialist remains bounded by the feature's impact.

## Mutation checks

The test specialist may deliberately introduce a fault only when:

- it is not obvious that a test detects its claimed regression; and
- the test protects a user story or critical edge case.

Run the mutation in an isolated disposable workspace that cannot affect other
reviewers or the implementation tree. Record the fault, expected detecting
test, and observed result. Discard the workspace afterward.

A mutation check proves a relationship between one test and one regression. It
does not turn mutation coverage into a general completion metric.

## Operating model

### 1. Reconstruct the review target

Read the Feature Brief, accepted Design, linked decisions, implementation,
tests, and project conventions. Determine the files changed by the feature and
the surrounding impact paths that specialists may need to follow.

### 2. Dispatch specialist reviews

Start one specialized sub-agent for each baseline lens. Start conditional
specialists when the feature touches their concern. Give every specialist its
narrow lens and the same canonical feature and change references.

Specialists may run existing tests and other read-only checks. Only the test
specialist may modify code, and only inside the isolated mutation workspace.

### 3. Assemble the report

Collect all candidate findings. The coordinator may merge duplicates and omit
candidates that are irrelevant, unsupported, contradicted by evidence, or
outside the feature's impact.

Omitted candidates do not appear in the report or a separate rejection log.
The coordinator must not turn curation into solution design or pretend that
the remaining candidates are verified.

### 4. Transition to Acceptance

Write the temporary Review report and request a controller-owned transition.
Acceptance starts in a fresh context and independently decides which candidates
are worth investigating before it verifies them.

Review does not present the candidate report directly to the user.

## Completion

Review is complete when:

- every required specialist has returned or is recorded as incomplete;
- the coordinator has assembled one candidate report;
- every retained finding has evidence and preliminary impact and severity;
- the report contains no recommendation or suggested solution;
- Review has made no repository changes outside an isolated mutation
  workspace;
- every mutation workspace has been discarded; and
- the controller can start Acceptance without the Review conversation.

## Failure behaviour

- Record missing specialist coverage instead of silently treating it as a
  clean result.
- Do not transition when report assembly or mutation cleanup fails.
- Leave uncertain but supported observations as candidates for Acceptance.
- Omit unsupported, unrelated, contradicted, and duplicate findings.
- Do not repair a finding during Review.
- Do not ask the user to evaluate an unfiltered specialist output.

## Open questions

The workflow still needs to define:

- the exact skills and prompts for each specialist;
- concurrency and capacity limits for specialist sub-agents;
- the preliminary impact and severity scales;
- retry behaviour when a specialist fails;
- the Review report schema and storage location; and
- the isolated mutation-workspace mechanism.
