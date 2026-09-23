# Acceptance Report

Status: Draft

## Purpose

An Acceptance Report records one Acceptance pass for one feature at one Git
revision. It preserves verified findings, user guidance, routed follow-up work,
and later dispositions beside the Feature Brief.

## Ownership and cardinality

- Acceptance creates one report for every pass, including a clean pass.
- The report lives in the same feature folder as the Feature Brief.
- Its filename contains the pass date and short Git SHA.
- The report records the full Git SHA internally.
- Later workflow steps and the user update findings they work on.
- Reports remain after the feature is complete.

For example:

```text
acceptance-2026-09-22-a1b2c3d.md
```

## Authority

The report is authoritative evidence of what Acceptance evaluated, what the
user decided, and the current disposition of its findings. It is not authority
for feature behaviour or architecture.

Behavioural changes must return through Shape and update the Feature Brief.
Architectural changes must return through Design and update code or an ADR when
required.

## Contains

- feature identity and Feature Brief location;
- Acceptance date and reviewed full Git SHA;
- pass outcome and feature status at the end of the pass;
- verified findings retained from the temporary Review report;
- evidence, independently assessed impact, and severity for each finding;
- grouping into broader topics where several findings share a cause;
- user guidance without generated recommendations;
- the workflow step associated with required work;
- the current disposition of each finding; and
- later evidence or notes needed to understand an updated disposition.

Possible dispositions include completed, ignored, outdated, and reassigned.
The vocabulary may expand when a workflow step needs a more accurate state.

## Does not contain

- Review candidates that Acceptance chose not to investigate;
- findings Acceptance could not substantiate as defects;
- generated recommendations or suggested solutions;
- copies of unresolved findings from older reports;
- a replacement feature specification or implementation plan;
- complete Review, Acceptance, or remediation conversations; or
- unrelated repository issues.

## Lifecycle

Acceptance creates a new report for each pass. A newer report does not replace
or rewrite an older one.

Unresolved findings stay in the report that first recorded them. When a
workflow step later picks up an item, it evaluates dependencies and stale
assumptions, then updates that item. The step and the user may remove findings
that have become outdated or irrelevant.

The feature remains unfinished while a report contains required unresolved
work. The user may decide that remaining items do not justify more work and
mark the feature complete. Reports remain beside the Feature Brief for later
reference after completion.
