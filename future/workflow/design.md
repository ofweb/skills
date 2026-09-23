# Design

Status: Draft

## Purpose

Design turns one ready [Feature Brief](../documents/feature-brief.md) into a
small, explicit implementation structure. It leaves a fresh Implementation
context with clear code contracts and a mechanically sound repository.

When several designs satisfy the agreed behaviour, prefer the design that
requires less unrelated repository context to understand and change safely.

Design is collaborative and requires explicit user acceptance. It never starts
the autonomous delivery chain on its own.

## Responsibilities

Design:

- verifies that the selected Feature Brief is ready and internally consistent;
- starts only from a clean working tree and a repository that passes its
  complete compile, test, lint, formatting, and prose checks;
- inspects existing code, tests, concepts, dependencies, and ownership before
  adding structure;
- traces every significant design element to agreed behaviour or a durable
  constraint;
- presents consequential design problems and asks the user for guidance;
- makes ordinary, local, reversible technical choices without interrupting the
  discussion;
- expresses the agreed structure primarily through code;
- preserves non-obvious intent in types, comments, or durable references;
- creates an [ADR](../documents/adr.md) when a durable architectural choice
  meets the ADR threshold;
- evaluates whether an independent remote critique is warranted;
- keeps the repository mechanically green; and
- obtains explicit user acceptance before Implementation.

Design does not:

- recommend an architecture or present an option menu;
- change feature behaviour, scope, stories, or acceptance criteria;
- implement the complete feature;
- create speculative abstractions for possible future work;
- produce a parallel prose implementation plan;
- write a full feature test suite for Implementation; or
- continue into Implementation in the same model context.

## Inputs

Design reads only the context needed for the selected feature:

- one ready Feature Brief;
- linked [Direction](../documents/direction.md),
  [Context](../documents/context.md), [PDR](../documents/pdr.md), and ADR
  material;
- the current code and nearby tests;
- repository build, format, lint, and test conventions;
- relevant research or external constraints; and
- evidence returned by an earlier Implementation attempt, when Design is being
  revisited.

Design never receives a group of features. Related ready briefs provide context
only when their boundaries constrain the selected feature.

## Outputs and authority

| Output | Meaning |
| --- | --- |
| Code structure | The accepted implementation baseline: ownership, boundaries, types, signatures, errors, and effect seams needed by the feature |
| ADR | Durable architectural reasoning that code cannot preserve safely by itself |
| Code comments and links | Local explanation of non-obvious constraints or deliberate choices |
| Feature Brief clarification | Non-material wording or link correction that leaves behaviour, scope, stories, and acceptance criteria unchanged |
| Workflow state | Design acceptance, relevant artifacts, and the next responsibility |

Implementation follows the accepted baseline. It may choose local implementation
details inside that baseline but must not silently redesign it.

## Collaboration model

Mike begins consequential design discussions by presenting the problem:

- what repository evidence exposed it;
- which agreed behaviour or constraint it affects;
- why ordinary local judgement cannot resolve it safely; and
- what would be settled implicitly if work continued.

Mike then asks the user for guidance. It does not lead with a proposed
architecture, a list of alternatives, or a preferred answer.

After the consequential choices are understood, Mike expresses them as a
working code baseline. The user may question or revise that structure before
accepting Design.

Ordinary choices that are constrained, local, reversible, and do not change a
durable boundary remain Mike's responsibility. A high-impact question that
must stop Design may invoke [Decision](decision.md).

## Operating model

### 1. Verify the repository baseline

Before Design starts, confirm that the working tree has no uncommitted or
untracked changes. Then run the repository's complete compilation or type
check, test suite, lint checks, formatting checks, and `prose-check`. Prose
validation covers all eligible project text, not only text changed by the
selected feature.

Design starts only from a known-good repository. Record the baseline results so
later steps can distinguish pre-existing failures from feature changes.

If the working tree or a baseline check fails, stop and inform the user. Do not
repair, commit, stash, discard, or otherwise change the repository. The user
may request repair through a separate skill.

### 2. Verify the feature input

Read the selected Feature Brief and every linked decision or constraint needed
to understand it. Check that its stories and acceptance criteria describe one
coherent feature and do not leave a behavioural choice for Design.

If the brief is not ready, stop Design and return to Shape.

### 3. Inspect repository reality

Locate the existing owners, concepts, representations, call paths, effects, and
tests connected to the feature. Search before adding a type, helper, service,
manager, adapter, trait, configuration form, or other abstraction.

Unexpected breadth or complexity is evidence. Surface it when it suggests that
the feature boundary, accepted behaviour, or current architecture was
misunderstood.

### 4. Trace behaviour to structure

Check both directions:

```text
agreed behaviour or constraint → required design element
design element → agreed behaviour or constraint
```

Every important behaviour needs a plausible implementation path. Every
significant design element needs a behavioural or architectural reason.

### 5. Resolve consequential design problems

Present one concrete problem at a time and ask the user for guidance. Examine
ownership, dependency direction, lifecycle, persistence, state, error
behaviour, security boundaries, and compatibility when the feature makes them
relevant.

Expose consequential premises by asking what must be true for the emerging
design to work. Verify repository facts and investigate external facts rather
than silently treating assumptions as constraints.

### 6. Express the design in code

Use the smallest code structure that makes the implementation target explicit.
Depending on the feature and language, Design may add or revise:

- module and responsibility boundaries;
- types, enums, and validated data shapes;
- important function signatures;
- interfaces or traits when they protect a real boundary;
- explicit inputs, outputs, and error shapes;
- effect boundaries;
- selective stubs; and
- test seams or minimal test scaffolding.

The code must state clearly which feature behaviour remains unimplemented.
Design must not disguise implementation work as structural setup.

### 7. Verify the baseline

Before asking for acceptance:

- compile or type-check the repository;
- run existing tests;
- run configured format and static checks;
- confirm that Design introduced no failing feature tests;
- inspect the designed area for accidental feature implementation or ambiguous
  stubs; and
- verify that a fresh context can locate the implementation target from the
  Feature Brief, code, and linked decisions.

### 8. Evaluate the need for independent critique

Use an independent remote critique when the design is large, complex, high-risk,
crosses important boundaries, or contains uncertainty that benefits from a
fresh review. Skip it for clearly small, local designs. Ask the user when the
need for evaluation is unclear.

The critique looks for unsupported assumptions, missing behaviour, unclear
ownership, poor dependency direction, unnecessary abstraction, duplicate
concepts, hidden lifecycle or state coupling, tangled effects, and artificial
test seams.

Treat findings as candidates. Verify them against repository evidence before
returning them to the Design discussion. Re-evaluate material revisions only
when the revised design still meets the critique threshold.

### 9. Obtain user acceptance

Present the resulting code baseline, linked ADRs, verified evaluation findings,
and any remaining constraints. The user must explicitly accept Design.

Acceptance authorizes the autonomous Implement → Review → Acceptance chain. It
does not authorize behaviour or architecture outside the accepted artifacts.

### 10. Transition to Implementation

Persist durable knowledge, run documentation and mechanical checks, and request
a controller-owned transition. Implementation starts in a fresh context from
repository state.

Design and Implementation never continue in the same model context.

## Design principles

### Local comprehensibility

Prefer predictable ownership, explicit dependencies, canonical representations,
small interfaces, and feature-local code. Minimize the unrelated context needed
to modify one behaviour safely.

### Logic and effects

Keep meaningful decision logic independent of I/O when that separation reduces
reasoning cost or improves testability. Keep networking, persistence, clocks,
hardware, and other effects at explicit boundaries. Do not force every feature
into a particular architectural pattern.

### Types preserve knowledge

Use validated or state-specific types when they prevent real ambiguity or
invalid states. Do not add wrappers or lifecycle types merely to appear
strongly typed.

### High threshold for abstraction

Treat duplication as evidence to investigate, not an instruction to abstract.
Share code when it represents the same domain meaning, has an appropriate owner,
and reduces context or drift. Small obvious duplication may remain when a shared
abstraction would add more concepts than it removes.

### Comments preserve non-obvious intent

Prefer structural clarity through types and APIs. Add concise comments when a
fresh context could not recover why ordering, duplication, validation, or an
unusual implementation choice is deliberate.

Link ADRs, PDRs, Feature Briefs, or stories when the full reasoning belongs in a
durable document. A local comment must still explain why the reference matters.

## Feature Brief changes

Design may correct wording, links, or other non-material clarification in the
Feature Brief when agreed behaviour, scope, stories, and acceptance criteria do
not change. Include those changes in the user's Design acceptance.

If Design exposes a material behavioural change, remove the brief's ready status
and return to Shape. Design must not use a clarification edit to take ownership
of feature behaviour.

## Returning from Implementation

When Implementation provides evidence that invalidates the accepted design,
Design reopens in a fresh collaborative context. Read the verified evidence,
revise the code baseline and affected ADRs to reflect that evidence, rerun
relevant evaluation, and obtain explicit user acceptance again.

Do not preserve a stale design because implementation has already invested work
in it.

## Completion

Design is complete when:

- the selected Feature Brief remains ready;
- agreed behaviour and constraints trace to the code baseline;
- significant design elements trace back to behaviour or durable decisions;
- existing ownership and reuse were investigated;
- consequential assumptions are resolved or explicitly preserved;
- required ADRs and comments exist;
- any required remote critique was verified and resolved;
- compilation or type checking passes;
- existing tests pass;
- formatting and configured static checks pass;
- the user explicitly accepts the baseline;
- workflow state identifies the accepted artifacts; and
- the controller can start Implementation without the Design conversation.

## Failure and interruption behaviour

- Return to Shape when accepted behaviour is ambiguous, incomplete, or must
  change.
- Do not start Design when the working tree is not clean or a repository
  baseline check fails. Report the problem without repairing it.
- Remain in Design when the architecture is unresolved or the baseline is not
  mechanically green.
- Invoke Decision only for a high-impact question that must stop Design.
- Ask the user whether remote evaluation is warranted when its value is unclear.
- Do not transition when the user has not accepted the design.
- Rerun Design after material implementation evidence invalidates the baseline.

## Open questions

The workflow still needs to define:

- how accepted code contracts are identified in workflow state;
- permitted stub patterns for each supported language;
- the exact Implementation-to-Design return outcome; and
- how Design acceptance is recorded and later invalidated.
