---
name: implement
description: Implement one accepted Design from a ready Feature Brief. Complete behaviour in small tested chunks while preserving the reviewed code contracts.
---

# Implement

Implement one accepted Design in a fresh context. Read the ready Feature Brief, accepted code structure, linked decisions, nearby code and tests, and repository checks. The Design conversation is not an input.

## Reconstruct the target

Find the Design commit and every designed stub. Use that commit as the implementation diff boundary. Confirm that its baseline is mechanically sound before attributing a failure to new work. Identify the complete feature behaviour from the Brief and the reviewed contracts from code and linked decisions.

Implement owns algorithms, control flow, private helpers and types, ordinary local data structures, constants, test fixtures, and restructuring inside an accepted component. A Design-created declaration can change when the change would not have mattered during Design review. Do not grow a second architecture beneath the reviewed one.

Return to Design when implementation requires a new architectural abstraction or a significant change to domain types, signatures, ownership, component boundaries, data flow, errors, effect boundaries, persistence formats, protocols, or concurrency. Return to Shape when required behaviour, scope, a story, or an acceptance criterion is missing, ambiguous, or wrong. Do not create an ADR or PDR within Implement.

## Work in small behaviour chunks

Read [simple-code](../simple-code/SKILL.md) before the first chunk. Apply it when choosing algorithms, helpers, local types, and effectful code within the accepted component. Keep each change easy to understand on its own. During cleanup, remove unnecessary indirection without building a new abstraction from speculative reuse.

Choose one coherent piece of feature behaviour that can be implemented and checked without leaving broken work behind. Understand its purpose, callers, dependencies, and regression risk before editing. Select a test level that protects the behaviour: focused tests for local logic and boundary tests when behaviour crosses a meaningful boundary.

For each chunk:

1. Write or update the relevant test. Confirm its intended failure when practical. If it already passes, explain why it still protects the new behaviour.
2. Implement the smallest complete behaviour within the accepted Design.
3. Run the focused test, compile or type-check, lint, and format. Fix failures before starting another chunk.
4. Simplify the code just changed without adding speculative abstractions. Check it against the Feature Brief and reviewed contracts.

Keep the chunk small enough that feedback arrives while the reason for the code is still fresh. Broaden integration checks as paths become complete. Fix ordinary compiler, test, lint, formatting, fixture, and integration problems autonomously.

If evidence invalidates an accepted contract, stop that path and return the problem to its owner. Include what the contract implied, what code or tests revealed, and why local implementation cannot solve it. If local investigation stops producing information, explain the concrete obstacle and ask the user for guidance. Do not silently change behaviour or architecture to get past it.

## Verify completion

Implement every designed stub and target. Run the complete test suite, compile or type-check, and pass configured lint and formatting checks. Inspect the designed area for unfinished code. Passing mechanical checks establishes readiness for Review; it does not prove feature correctness or test adequacy.

Record the Design commit SHA and identify the changed code and tests. Request the Implement to Review transition when a workflow controller is available. Otherwise tell the user to start Review in a fresh context from repository state. Do not carry a prose handoff or continue into Review in this context.
