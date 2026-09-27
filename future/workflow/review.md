# Review

Status: Draft

## Purpose

Review evaluates one completed implementation in a fresh context. It checks
the feature against durable project intent, reruns mechanical checks, and
investigates whether the change made the system harder to understand or change.

The Design commit identifies where Implementation started. It is a diff
boundary, not a Review authority. A final implementation may differ from that
code without producing a finding when it still satisfies the Feature Brief and
durable decisions.

Review uses several focused subagents and assembles their candidate findings
into one temporary report for Acceptance.

## Responsibilities

Review:

- reconstructs the feature from durable repository state;
- identifies the reviewed snapshot and the change since the Design commit;
- independently runs relevant compile, test, lint, formatting, prose, and
  other configured checks;
- traces the feature's effects beyond changed files when needed;
- assigns narrow responsibilities to several specialist subagents;
- requires exact evidence and preliminary impact and severity for candidates;
- curates duplicate and unsupported candidates into one report; and
- hands that report to Acceptance in a fresh context.

Review does not:

- treat Design-created code as a requirement for the final structure;
- trust Implementation's check report instead of rerunning checks;
- modify production code, tests, documents, or accepted contracts;
- suggest fixes or preferred responses;
- treat a specialist's judgement as a verified defect;
- review unrelated repository health; or
- decide that the feature is accepted.

## Inputs and authority

Review reads:

- the ready [Feature Brief](../documents/feature-brief.md) for agreed behaviour,
  stories, and acceptance criteria;
- linked [PDRs](../documents/pdr.md) for product decisions and
  [ADRs](../documents/adr.md) for architectural decisions;
- relevant [Direction](../documents/direction.md) for project intent and
  [Context](../documents/context.md) for terms and invariants;
- the Design commit SHA to locate the implementation change boundary;
- the completed code, tests, and affected callers and integration paths; and
- project check commands and style rules.

Review does not inherit the Design or Implementation conversation. It does not
use the Design commit as authority for a finding. A finding needs a durable
contract or a concrete defect in the completed implementation.

## Report

Write one temporary report at:

```text
.workflow/review/<feature-id>-<revision>.md
```

The report is workflow state and the directory is gitignored. It survives a
context clear, process exit, or machine reboot. Acceptance transfers evidence
for retained findings and deletes the temporary report. A future controller
may change the transport without changing these responsibilities.

The report identifies the feature, Design commit, reviewed revision and working
tree state, change scope, mechanical checks and results, specialists that ran
or were incomplete, and retained candidates. Each candidate gives its source
specialist, exact location, expected and observed behaviour, supporting code
or durable contract, plausible consequence, and preliminary impact and
severity. The report contains no recommendations or suggested solutions.

## Scope and checks

Follow callers, callees, types, state, and integration paths through the
repository when the feature can affect them. A problem without a causal or
behavioural link to this feature is outside Review.

First identify the exact snapshot. Record the Git revision and working tree
state when implementation is uncommitted. A Git SHA alone does not identify
uncommitted changes. Compare the feature against the Design commit to locate
the implementation diff.

Run the repository's relevant compile or type check, complete test suite,
lint, formatting check, and other configured mechanical checks against the
reviewed snapshot. Run prose checks on changed comments and documentation.
Use check-only commands. If a check would modify the implementation tree, run
it in isolation or record it as incomplete. Record failures and incomplete
checks with evidence. Do not repair the feature during Review.

## Focused specialists

Give each specialist the same feature, durable artifacts, snapshot, and change
boundary. Give each a limited, coherent responsibility. Run specialists in
batches when capacity is limited. Each returns evidence-backed candidate
findings without editing code or proposing a response.

### 1. Feature behaviour and tests

Compare every story and acceptance criterion with the implemented behaviour.
Find missing, changed, or extra behaviour. Check important failures, edge
cases, and integration paths. Check whether tests detect meaningful
regressions. Recheck affected old tests for stale expectations. Do not use
test count or line coverage as proof of behavioural coverage.

### 2. Correctness and integration

Inspect algorithms, conditions, state transitions, cleanup, and error
propagation. Trace changed code through callers and callees. Check data shapes,
protocols, neighbouring implementations, and compatibility for drift.

### 3. Types and boundaries

Check type safety, domain distinctions, ownership, and invalid states. Look
for unsafe escape hatches and weak values used before their invariants hold.
Check that external input becomes meaningful domain types at trust boundaries.
Check constructors and deserializers for paths that bypass those invariants.

### 4. Simple code

Read [simple-code](../../simple-code/SKILL.md) and give the same path to this
specialist. Inspect changed responsibilities, data and control flow,
dependencies, effects, abstractions, duplication, and reasoning cost. A
candidate needs a concrete consequence for understanding or future change.
Do not report a preference for fewer lines or a different style.

### 5. Prose and comments

Check changed documentation and comments against code and durable decisions.
Find stale, misleading, redundant, and unclear prose. Preserve comments that
explain non-obvious intent. Check public API contracts and links. When a
project style guide exists, cite its exact rule. Do not substitute reviewer
preference for a missing rule.

Add separate security, concurrency and state, persistence and lifecycle,
protocol compatibility, or domain specialists when the feature exposes those
concerns. Keep every specialist within the feature's impact.

## Mutation checks

The behaviour and test specialist may introduce a deliberate fault only when
it is unclear whether a test detects a story regression or critical edge
case. Run the fault in an isolated disposable workspace. Record the fault,
expected detecting test, and observed result. Discard the workspace. Skip the
mutation when isolation is unavailable.

## Assemble and hand off

Merge duplicates. Omit candidates contradicted by evidence, unsupported,
unrelated, or outside the feature's impact. Preserve supported uncertainty as
a candidate. Record required specialist coverage that did not run as
incomplete. Do not turn curation into solution design or claim that retained
findings are verified.

Write the report and request a controller-owned transition to Acceptance. If
the controller is unavailable, give the report path for a fresh Acceptance
context. Do not present the unverified candidate report directly to the user.

Review is complete when required checks and specialists ran or are recorded as
incomplete, the report is assembled, and every mutation workspace is gone.
Do not transition when report assembly or cleanup fails.

## Open questions

The workflow still needs to define:

- the preliminary impact and severity scales;
- retry behaviour when a specialist fails;
- the isolated mutation-workspace mechanism; and
- how a controller replaces the report transport.
