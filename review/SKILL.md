---
name: review
description: Review one completed feature against durable project intent with focused specialists and independent checks, then prepare candidates for Acceptance.
---

# Review

Review one completed feature in a fresh context. Reconstruct its intent from the Feature Brief, linked PDRs and ADRs, relevant Direction and Context documents, and current code. Use the Design commit only to locate the implementation diff. A difference from the Design code is not a finding unless it violates durable intent or causes a concrete problem. Do not use the Implementation conversation or its check reports as evidence.

## Establish the reviewed snapshot

Record the feature ID, Design commit SHA, reviewed revision, and change boundary. If implementation work is uncommitted, record the working-tree state as part of the snapshot. Follow affected callers, callees, types, state, and integration paths when the change can affect them. Do not audit unrelated code.

Independently run the repository's configured compile or type check, complete test suite, lint, formatting check, and other relevant mechanical checks against this snapshot. Use check-only commands. If a check would modify the implementation tree, run it in isolation or record it as incomplete. Run prose checks on changed comments and documentation. Report failed or incomplete checks with their evidence; do not repair the feature.

## Dispatch focused specialists

Use several narrow subagents. Give each the same feature, durable artifacts, snapshot, and change boundary, but only its own review responsibility. Run them in batches when capacity is limited. A specialist returns evidence-backed candidate findings and does not edit production code or propose fixes.

1. **Feature behaviour and tests:** Compare stories and acceptance criteria with observed behaviour. Find missing or extra behaviour, weak tests, important failures, and edge cases. Identify the regression each important test detects. Recheck affected old tests.
2. **Correctness and integration:** Check algorithms, conditions, state transitions, errors, cleanup, callers, callees, protocols, and compatibility.
3. **Types and boundaries:** Check type safety, domain distinctions, invalid states, ownership, and parsing of weak input at trust boundaries. Check constructors that could bypass invariants.
4. **Simple code:** Read [simple-code](../simple-code/SKILL.md) and give this exact path to the specialist. Apply it to the changed responsibilities, data and control flow, dependencies, effects, abstractions, duplication, and reasoning cost. Require a concrete consequence instead of a style preference.
5. **Prose and comments:** Check changed documentation and comments against code and durable decisions. Find stale, misleading, redundant, or unclear prose. Preserve comments that explain non-obvious intent. Cite an applicable project style rule when one exists.

Add separate specialists for security, concurrency, persistence or lifecycle, protocol compatibility, or domain-specific risks when the feature exposes them. Keep each specialist within the feature's impact. Record missing required coverage as incomplete, not clean.

The test specialist may introduce a deliberate fault only when a critical test's effectiveness is unclear. Use an isolated disposable workspace, record the fault and result, and discard the workspace. Skip this check when isolation is unavailable.

## Curate candidates

Each candidate identifies its specialist, exact location, expected and observed behaviour, supporting code or durable contract, plausible consequence, and preliminary impact and severity. Mechanical failures also identify the check and result. Keep supported uncertainty visible. Merge duplicates and omit claims that are unsupported, contradicted, unrelated, or outside the feature's impact. Do not verify findings on Acceptance's behalf, recommend solutions, or decide that the feature is complete.

## Hand off to Acceptance

Write one temporary report at `.workflow/review/<feature-id>-<revision>.md`. Include the reviewed snapshot, Design diff boundary, check results, specialist coverage, and retained candidates. Keep this directory out of Git. The report is workflow state, not permanent project documentation. Acceptance transfers relevant evidence and deletes it. Give the report path for a fresh Acceptance context; do not present unverified candidates directly to the user or continue into Acceptance here.
