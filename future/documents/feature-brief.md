# Feature Brief

Status: Draft

## Purpose

A Feature Brief carries a feature from durable working understanding to an
agreed behavioural contract for Design. Shape creates and updates it throughout
the discussion rather than waiting until the feature is complete.

## Ownership and cardinality

- Each substantial feature has one Feature Brief.
- Shape creates, updates, and establishes readiness with the user.
- Design may make non-material wording or link clarifications and includes them
  in explicit Design acceptance.
- Related features keep separate briefs even when Shape discusses them together.
- Design receives exactly one ready Feature Brief at a time.
- Every Acceptance Report is stored beside the Feature Brief for the feature it
  evaluates.

## Lifecycle and authority

```text
Backlog item → Draft Feature Brief → Ready Feature Brief → Design
```

A draft is durable working memory, not accepted behaviour. It may contain
tentative boundaries, open questions, and unverified assumptions when they are
marked clearly.

A ready brief is authoritative for the feature behaviour entering Design. File
existence, length, or complete-looking sections do not establish readiness.
Shape and the user must agree explicitly.

If later evidence invalidates ready behaviour, the workflow must remove its
ready status before changing the contract. The exact return transition remains
to be defined.

Design returns the brief to Shape when behaviour, scope, stories, or acceptance
criteria must change. Design may not hide such a change as clarification.

Acceptance Reports do not change the brief's authority. A finding that requires
different feature behaviour must return to Shape before the brief changes.

## Contains

- status and feature identity;
- goal and intended value;
- at least one user or system story;
- expected observable behaviour;
- acceptance criteria linked to stories or named constraints;
- relevant failure and boundary behaviour;
- permissions, persistence, lifecycle, and compatibility where observable;
- scope and explicit non-goals;
- relationships with neighbouring features;
- links to shared Direction, Context, PDR, or ADR material; and
- open questions and assumptions while the brief is a draft.

Each story identifies an actor, situation, intent or action, and observable
result. Stories do not require rigid "As a user" wording.

## Acceptance criteria

- Every story has acceptance coverage.
- Every criterion traces to a story or named feature-wide constraint.
- Criteria describe observable behaviour, not implementation structure or test
  code.
- Criteria include important failure and boundary behaviour.
- Criteria spanning stories within one feature live in that brief's
  feature-wide acceptance section.

When behaviour or a constraint applies to several features, record it once in
the Direction document or a PDR or ADR, according to its meaning. Every affected
Feature Brief must link to that canonical document.

## Does not contain

- internal APIs, modules, schemas, classes, or data structures;
- library or framework selection;
- an implementation plan or engineering task list;
- test implementation details;
- conversation history;
- copied shared decisions or constraints; or
- speculative future behaviour outside the feature boundary.

## Ready boundary

A brief is ready when its feature is a small coherent vertical slice, its
stories and acceptance criteria cover the agreed behaviour, its scope and
non-goals are intentional, material assumptions are resolved or safely
deferred, required shared documents are linked, and no open question can
materially change the feature.
