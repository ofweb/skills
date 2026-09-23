# Implement

Status: Draft

## Purpose

Implementation completes one accepted Design through small test-driven loops.
It starts in a fresh context and normally runs unattended until the feature is
mechanically ready for independent Review.

Design is already complete. Implementation fills in the accepted structure; it
does not revisit behaviour or architecture while coding.

## Responsibilities

Implementation:

- reconstructs the feature from durable repository state;
- divides the accepted design into small coherent implementation chunks;
- understands each chunk's purpose and place in the feature before changing it;
- writes tests appropriate to the chunk's role and regression risk;
- implements tests and production code together in short feedback loops;
- runs focused tests, compilation, linting, and formatting throughout the work;
- resolves ordinary coding, tooling, and integration failures autonomously;
- uses remote consultation within its strict delegation limits when local
  investigation stops producing information;
- returns invalid behaviour to Shape and invalid architecture to Design; and
- hands a mechanically complete feature to Review in a fresh context.

Implementation does not:

- change the accepted feature behaviour;
- alter accepted design structure to make implementation easier;
- create a new ADR or PDR;
- ask the user to approve ordinary implementation choices or successful loops;
- treat passing tests as proof that the feature is correct; or
- continue when evidence shows that the accepted Design must change.

## Inputs

Implementation reads the minimum durable context needed for the selected
feature:

- the ready [Feature Brief](../documents/feature-brief.md), including its stories
  and acceptance criteria;
- the accepted Design expressed in code;
- linked [Direction](../documents/direction.md),
  [Context](../documents/context.md), [PDR](../documents/pdr.md), and
  [ADR](../documents/adr.md) material;
- nearby implementation, callers, and tests; and
- repository build, test, lint, and formatting conventions.

The Design conversation is not an input. Repository state must contain the
contracts and knowledge required to continue.

## Outputs and authority

| Output | Meaning |
| --- | --- |
| Implementation code | Completed behaviour inside the accepted Design |
| Tests | Focused protection chosen for each chunk's purpose and risk |
| Mechanical results | Evidence that the complete test, compile, lint, and formatting checks pass |
| Consultation record | Compact workflow instrumentation for any remote call and its result |
| Workflow state | The active feature, completion result, and Review transition |

Implementation may choose local details inside the accepted contracts. That
authority does not extend to revising designed signatures, ownership,
boundaries, errors, effects, or other accepted structure.

## Operating model

### 1. Reconstruct the implementation target

Read the Feature Brief, accepted code structure, linked decisions, and relevant
repository conventions. Locate every designed stub and the code paths in which
it participates.

Confirm that the accepted baseline is mechanically sound before attributing a
pre-existing failure to new work. If the target or behaviour cannot be
reconstructed from repository state, route the missing contract to its owner.

### 2. Select a small coherent chunk

Choose one function or a few closely related functions. Before writing a test,
determine:

- what purpose the chunk serves;
- how it fits the accepted solution;
- which callers and dependencies constrain it;
- what observable failure it could introduce; and
- which remaining feature behaviour it advances.

The chunk should be small enough that compiler, test, and lint feedback points
back to the current change.

### 3. Select tests by purpose

Use the test level that protects the chunk's role. Pure logic and plumbing may
need only focused unit tests. Behaviour that crosses a meaningful feature or
system boundary needs evidence at that boundary.

Do not require both unit and feature-path tests for every chunk. Do not write
the complete feature's tests before implementing its first part. Accumulate
coverage as the accepted design becomes executable.

### 4. Run the local feedback loop

For each chunk:

```text
understand the chunk and its feature role
    ↓
write the smallest useful test
    ↓
confirm that it fails for the intended reason
    ↓
implement the smallest complete change
    ↓
run the focused test
    ↓
compile or type-check
    ↓
lint and format
    ↓
run affected feature and integration tests
    ↓
perform small local cleanup
    ↓
repeat
```

Use the repository's configured tools. Run cheap checks immediately and broaden
the test scope as implemented paths accumulate. A test that passes before its
implementation must be corrected or justified before continuing.

### 5. Preserve the accepted Design

Prefer leaving all Design-created structure unchanged. Fill designed stubs and
add only the private implementation needed to make their contracts real.

When implementation evidence shows that a designed signature, boundary,
ownership rule, error shape, effect seam, or other accepted structure must
change, stop and return to Design. Provide:

- what the accepted Design implied;
- what the repository or implementation revealed;
- the code, test, or compiler evidence;
- why the problem cannot be solved within the accepted structure; and
- which part of Design needs reconsideration.

Return to Shape instead when the evidence shows that feature behaviour, scope,
a story, or an acceptance criterion is missing, ambiguous, or wrong.

### 6. Escalate implementation difficulty

Continue local investigation while it produces new information. When a
concrete implementation problem remains stuck, Implementation may invoke the
separate remote-consultation skill automatically if remote use has been
configured and authorized.

Remote consultation is read-only input. The request contains only the current
chunk, accepted contracts, relevant local findings, failure evidence, and a
narrow question. Mike owns all edits and verifies the advice locally.

Only one remote call is allowed for one problem. A changed symptom from the
same unresolved cause does not create another allowance. The
remote-consultation skill owns eligibility, model selection, capacity checks,
call quotas, cooldown periods, and token-usage accounting.

If the call does not unblock the work, present the problem to the user. Explain
what was attempted, what the remote model contributed, and why the failure
remains. Resume from the user's guidance without turning the interruption into
a formal [Decision](decision.md). If the user indicates that the problem needs
a broader discussion, ask whether it merits invoking Decision.

Remote advice that requires changed behaviour or architecture is evidence for
Shape or Design, not permission to bypass them.

### 7. Verify mechanical completion

Before requesting Review:

- implement every stub and target created by Design;
- run the complete test suite and resolve every failure;
- compile or type-check the project successfully;
- pass all configured lint checks; and
- pass all configured formatting checks.

Inspect the designed area directly for unfinished implementations. Do not rely
only on tests to reveal an unused stub.

These checks establish implementation completion, not feature correctness or
test adequacy. Review evaluates those independently.

### 8. Transition to Review

Record the mechanical results and request a controller-owned transition.
Review starts in a fresh context from the Feature Brief, accepted Design,
implementation, tests, linked decisions, and workflow state.

Implementation and Review never continue in the same model context.

## Autonomy boundaries

Implementation remains autonomous while work is constrained by accepted
behaviour and Design. It fixes compiler errors, failing tests, lint failures,
fixture problems, misunderstood helpers, and integration mistakes without user
approval.

It stops autonomous work when:

- behaviour must be clarified or changed;
- accepted Design structure must change;
- remote consultation and local investigation have not resolved an
  implementation problem;
- continuing requires authority outside the accepted feature; or
- an external condition prevents progress.

Formal Decision is not the default response to an implementation stop. Shape
and Design own invalid contracts. The user normally provides direct guidance
for exhausted implementation problems.

## Completion

Implementation is complete when:

- every designed stub and implementation target is complete;
- the complete test suite passes;
- compilation or type checking passes;
- linting passes;
- formatting checks pass;
- no unresolved evidence requires a return to Shape or Design; and
- the controller can start Review without the Implementation conversation.

Review begins by determining whether the accepted Design and completed
implementation actually provide the feature and whether the added tests are
adequate.

## Failure and interruption behaviour

- Keep ordinary implementation failures inside the local feedback loop.
- Use at most one remote consultation for the same problem.
- Ask the user for guidance when that consultation does not unblock the work.
- Ask about Decision only after the user identifies a need for broader
  discussion.
- Return changed feature behaviour to Shape.
- Return changed accepted structure to Design with concrete evidence.
- Do not transition while any designed stub or mechanical check remains
  incomplete.

## Open questions

The workflow still needs to define:

- the remote-consultation skill and its quota and accounting state;
- stable machine-readable implementation stop and escalation identifiers;
- how the controller identifies the complete repository test suite; and
- the exact Implementation-to-Design and Implementation-to-Shape transition
  payloads.
