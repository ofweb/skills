---
name: review
description: Review one completed feature from a fresh context with independent specialist lenses, then prepare an evidence-based candidate report for Acceptance.
---

# Review

Review one completed implementation from a fresh context. Read the ready Feature Brief, accepted Design in code, linked decisions, implementation diff, tests, and mechanical results. Do not use the Implementation conversation as evidence. Review reports candidate problems; Acceptance decides which candidates warrant verification and user attention.

## Bound the review

Identify the feature, reviewed Git revision, and implementation change boundary. If implementation work is uncommitted, record the working-tree state as part of the reviewed snapshot. A Git SHA alone does not identify those changes. Follow affected callers, callees, types, state, and integration paths when they can reveal an effect of this change. Do not audit unrelated repository code.

Use one specialized subagent for each applicable lens below. Give each the same feature and revision references and one narrow responsibility. Run agents in batches when capacity is limited. Each specialist inspects evidence and returns candidate findings without editing code or proposing fixes. Record a required lens as incomplete when it cannot run; do not interpret missing coverage as a clean result.

## Specialist lenses

- **Feature compliance:** Compare every story and acceptance criterion with the implementation. Find missing, changed, or extra behaviour.
- **Test effectiveness:** Check feature paths, failures, edge cases, and integration paths. Identify the regression each important test detects. Check whether affected old tests still encode valid behaviour. Do not use test count or coverage percentage as proof.
- **Correctness:** Check algorithms, conditions, state transitions, boundaries, cleanup, error propagation, and sibling paths.
- **Integration and contracts:** Trace callers and callees for signature, data shape, effect, error, protocol, and compatibility drift.
- **Simple code and structure:** Apply `simple-code`. Check responsibility, ownership, dependencies, hidden effects, unsafe duplication, unnecessary abstraction, and difficulty of future change. Require a concrete consequence, not a style preference.
- **Comments:** Check changed comments against nearby code and durable decisions. Keep comments that preserve non-obvious intent. Check API contracts and links. Use a dedicated comment-review skill when available; otherwise give this lens to a specialist directly.
- **Project style:** When a project style guide exists, cite its exact rule for each candidate. Record this lens as inapplicable when no guide exists. Do not substitute reviewer preference.
- **Type safety:** Check unsafe casts or escape hatches, nullability, unchecked boundary values, and values used before invariants hold.
- **Type design:** Check domain distinctions, valid states, ownership, canonical representations, and contradictory fields or flags.
- **Parse at boundaries:** Check that weak input becomes a domain type at the boundary, constructors preserve invariants, and internal code avoids repeated validation.

Add separate security, concurrency and state, persistence and lifecycle, or compatibility specialists when this feature exposes those concerns. Keep each specialist within the feature's impact.

## Gather evidence without changing the feature

Each candidate must identify its lens, exact location, expected and observed behaviour, supporting code or contract, plausible consequence, and preliminary impact and severity. A specialist's claim remains a candidate. Do not recommend a fix, change code, or decide feature acceptance.

The test specialist may use a deliberate fault only when test effectiveness is genuinely unclear for a story or critical edge case. Use an isolated disposable workspace that cannot affect the implementation tree or other reviewers. Record the fault and observed test result, then discard that workspace. Skip the mutation when isolation is unavailable.

Merge duplicate candidates and omit those contradicted by evidence, unsupported, unrelated, or outside the feature's impact. Preserve supported uncertainty as a candidate. Do not turn curation into solution design or claim that retained findings are verified.

## Hand off to Acceptance

Write one temporary report outside the implementation tree. Include the feature, reviewed snapshot, change scope, lenses run or missed, and retained candidates with evidence and preliminary impact and severity. Do not include recommendations. If no workflow controller exists, put the report in `/tmp` and provide its path for a fresh Acceptance context. Do not present unverified candidates directly to the user or continue into Acceptance in this context.
