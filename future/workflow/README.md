# Mike development workflow

Status: Draft

## Purpose

Mike combines continuous project steering, collaborative feature definition,
and an autonomous delivery chain. Repository state carries durable knowledge;
conversations and individual model contexts are disposable.

The workflow is not a linear checklist. Delivery has a normal forward path,
but decisions, discoveries, defects, and new evidence can interrupt or reroute
active work.

## Workflow model

```text
ideas, evidence, and completed work
                ↕
            Direction ↔ user
             ↙      ↘
   Direction document  Backlog
                           ↕
                         Shape ↔ user
                           ↓ one selected ready Feature Brief
                         Design ↔ user
                           ↓ accepted design
                      Implement
                           ↓
                         Review
                           ↓
                       Acceptance
                           ↓
                          Done
                           ↓
                  progression discussion
                           ↺ Direction and Backlog
```

Direction and Shape maintain the Backlog together. The Backlog is an artifact,
not a workflow step.

Decision can interrupt any active work:

```text
active work
    ↓ consequential uncertainty
save minimal pause state
    ↓
Decision discussion ↔ user
    ↓
persist durable outcome, if any
    ↓
resume the interrupted work or reroute to the responsible step
```

Research, experiments, remote consultation, documentation, and mechanical
checks are activities used within the workflow. They are not delivery stages.

## Project steering

### Direction

[Direction](direction.md) takes ideas, evidence, and learning from delivered work. Through
discussion with the user, it maintains a cohesive
[Direction document set](../documents/direction.md) describing the project's
intended end state.

Direction also creates and maintains the [Backlog](../documents/backlog.md) with
Shape. It may create a [PDR](../documents/pdr.md) when a durable product or
behavioural decision needs rationale beyond one feature.
It records relevant external links in [References](../documents/references.md).

Direction is ongoing project steering rather than the first step of every
feature. It does not turn the Direction document into a roadmap or progress
report. Direction itself never completes; individual discussions end after
their durable results are preserved.

The user starts Shape by naming the item or related features to discuss. That
active selection belongs to workflow state rather than the Direction document
or Backlog.

## Delivery

### Shape

[Shape](shape.md) turns Direction ideas and Backlog items into small coherent
features. It continuously updates draft [Feature Briefs](../documents/feature-brief.md)
and establishes readiness with the user.

One Shape round may refine several Backlog items or make a small related set of
Feature Briefs ready. It selects at most one ready brief for Design.

Shape may create:

- a PDR for durable product or behavioural decisions; and
- an [ADR](../documents/adr.md) only when architecture must be settled to
  establish feature feasibility, observable behaviour, or boundaries.

### Design

[Design](design.md) receives exactly one ready Feature Brief. Mike and the user decide how
the agreed behaviour should fit the repository.

Design expresses implementation structure primarily through code: types,
interfaces, module boundaries, function signatures, error shapes, selective
stubs, and test seams. It may create ADRs for durable architectural decisions.

The user explicitly accepts the design. That acceptance authorizes the
autonomous delivery chain.

Independent remote critique is conditional rather than mandatory. Use it for
large, complex, high-risk, cross-boundary, or materially uncertain designs. Ask
the user when its value is unclear.

### Implement

[Implementation](implement.md) completes the accepted design through small
test-driven loops. It selects one small coherent chunk at a time, understands
its role, chooses tests appropriate to its purpose, and uses immediate test,
compiler, lint, and formatting feedback.

It resolves ordinary coding, tooling, and integration problems autonomously.
When local investigation stops producing information, it may make one
authorized remote-consultation call for that problem. If the work remains
blocked, it presents the evidence to the user for guidance.

Implementation must not invent product behaviour or architecture. Evidence
that invalidates the accepted behaviour returns to Shape. Evidence that
invalidates the accepted architecture returns to Design.

Implementation does not create a new ADR autonomously. It returns the
architectural question to Design. It hands work to Review only after every
designed stub is implemented and the complete test, compile, lint, and
formatting checks pass.

### Review

[Review](review.md) starts in a fresh context. It runs each behavioural,
testing, correctness, integration, structural, comment, style, and type lens in
a specialized sub-agent. Specialists focus on the current change but may trace
its effects through the rest of the repository.

The Review coordinator curates candidate findings into one temporary report.
Each finding includes evidence and a preliminary impact and severity, but no
recommendation or suggested solution. Acceptance evaluates and verifies the
candidates independently.

### Acceptance

[Acceptance](acceptance.md) starts in another fresh context. It first decides which Review
candidates deserve investigation, then verifies those candidates rather than
trusting their specialist assessments. It may use focused remote help while
investigating.

Acceptance discusses verified findings with the user, starting with major
topics that may resolve several findings. It records the user's guidance and
routes needed work by owning workflow step. A report remains beside the
Feature Brief while its findings constrain current work.

When no verified finding deserves user attention and no earlier report still
requires work, Acceptance marks the feature complete without starting a
discussion or retaining a report. Required unresolved work leaves the feature
unfinished unless the user closes it.

## Collaboration and autonomy

| Work | Interaction model |
| --- | --- |
| Direction | Collaborative |
| Shape | Collaborative |
| Design | Collaborative |
| Implement | Autonomous after design acceptance |
| Review | Autonomous specialist investigation and report assembly |
| Implementation fixes | Autonomous within accepted behaviour and design |
| Acceptance | Independent evaluation, then collaborative when findings require guidance |
| Decision | Collaborative interruption |

Collaborative work is question-led and non-recommending. Mike contributes
evidence, challenges, and focused questions, but does not present option menus
or lead with a preferred answer. Consequential judgement remains with the user.

Mike returns control to the user when continuing requires a new product or
architectural decision, accepted behaviour is ambiguous, authority must expand,
or an external condition prevents progress. It does not pause for routine
implementation choices or verified defects that fit the accepted contracts.

## Decision interruptions

[Decision](decision.md) handles consequential uncertainty without becoming another stage in
the delivery sequence. Invoke it when choosing silently could change observable
behaviour, architecture, ownership, persistence, protocol, lifecycle, or
substantial completed work.

Decision may end with a resolved choice, a targeted investigation, an
experiment, or a return to an earlier collaborative step. It does not create a
decision record merely because it ran.

Route durable results by meaning:

- project direction → Direction document;
- feature-specific behaviour → Feature Brief;
- durable product or behavioural decision → PDR;
- durable architectural decision → ADR;
- stable terminology → [Context](../documents/context.md);
- implementation structure → code and tests; and
- local reversible choice → no durable document.

## Context boundaries and transitions

Each major change of responsibility starts in a fresh model context. The
workflow controller, not the model invoking `/clear`, owns the transition.
Until that controller is available, the user runs `/clear` after the active
step declares the transition. The next step reads canonical repository state.

See [Workflow transitions and state](transitions.md) for the shared boundary,
confirmation, routing, and failure requirements.

Before a transition, the active step:

1. writes durable knowledge to its canonical home;
2. verifies the step's completion conditions;
3. runs required document and mechanical checks; and
4. requests the transition.

The controller validates the request, records compact workflow state, ends the
current session, and starts the next responsibility from repository state.

Every transition first presents the completed step, changed artifacts, passed
checks, proposed next step, and a warning that the context will be cleared.
Most transitions wait for explicit user confirmation. Implementation may
continue directly to Review, and Review may continue directly to Acceptance.

Handoff state records the active feature, responsibility, outcome, return point,
and artifact locations. It is not a conversation summary or another project
document.

## Durable artifacts

| Artifact | Created or maintained by |
| --- | --- |
| Direction document | Direction |
| External references | Direction |
| Backlog | Direction and Shape |
| Feature Brief | Shape |
| PDR | Direction and Shape |
| ADR | Shape within its narrow boundary, and Design |
| Context | The collaborative step that resolves stable terminology |
| Code | Design and Implementation |
| Tests | Implementation, guided by Design seams and Feature Brief acceptance criteria |
| [Acceptance Report](../documents/acceptance-report.md) | Acceptance, then the responsible workflow steps and user |

See [Workflow documents](../documents/README.md) for authority, content, and
exclusion rules.

## Detailed guides

- [Direction](direction.md)
- [Shape](shape.md)
- [Design](design.md)
- [Implement](implement.md)
- [Review](review.md)
- [Acceptance](acceptance.md)
- [Decision](decision.md)
- [Workflow transitions and state](transitions.md)

## Open questions

The workflow still needs to define:

- Backlog item lifecycle and dependency semantics;
- whether an independent Shape critique is mandatory; and
- the workflow controller's exact state format, outcome identifiers, and
  validation interface.
