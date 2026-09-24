# Acceptance Report

Status: Draft

## Purpose

An Acceptance Report records verified findings and routed work from one
Acceptance pass at one Git revision while they remain relevant. It sits beside
the Feature Brief.

## Ownership and cardinality

- Acceptance creates one report for a pass with retained findings. A clean pass
  needs no lasting report.
- The report lives in the same feature folder as the Feature Brief.
- Its filename contains the pass date and short Git SHA.
- The report records the full Git SHA internally.
- Later workflow steps and the user update findings they work on.
- Remove a report when no finding in it constrains current work. Git preserves
  earlier passes.

For example:

```text
acceptance-2026-09-22-a1b2c3d.md
```

## Authority

While retained, the report is authoritative for its verified findings, user
guidance, and current disposition. It is not authority for feature behaviour
or architecture.

Behavioural changes must return through Shape and update the Feature Brief.
Architectural changes must return through Design and update code or an ADR when
required.

## Contains

- feature identity and Feature Brief location;
- Acceptance date and reviewed full Git SHA;
- current scope of unresolved follow-up;
- verified findings retained from the temporary Review report;
- evidence, independently assessed impact, and severity for each finding;
- grouping into broader topics where several findings share a cause;
- user guidance without generated recommendations;
- the workflow step associated with required work;
- the current disposition of each finding; and
- later evidence needed to understand an unresolved disposition.

Disposition identifies the current owner and whether follow-up is still
required. Remove findings once they no longer constrain current work.

## Does not contain

- Review candidates that Acceptance chose not to investigate;
- findings Acceptance could not substantiate as defects;
- generated recommendations or suggested solutions;
- copies of findings owned by another current report;
- a replacement feature specification or implementation plan;
- complete Review, Acceptance, or remediation conversations; or
- unrelated repository issues.

## Lifecycle

Acceptance creates a report when a pass retains findings. A later pass creates
a separate report only for newly retained findings. It may render earlier
findings obsolete; update or remove those records rather than keeping a pass
history in `.workflow/`.

Unresolved findings stay in the report that first recorded them. When a
workflow step picks up an item, it evaluates dependencies and stale assumptions,
then updates or removes that item. Remove the report when its remaining
findings are resolved, outdated, or irrelevant. Update links that pointed to it.

The feature remains unfinished while a report contains required unresolved
work. The user may decide remaining items do not justify more work and mark
the feature complete; remove reports that no longer constrain current work.

Aim for 250–500 words per report. The hard limit is 800 words per report.
Keep each finding to concise evidence, impact and severity, current disposition,
and routing needed later. Remove review transcripts, duplicate background,
obsolete findings, and completed history. Link to canonical behaviour or design
instead of repeating it. `workflow-document-check` enforces the limit for
each retained report.
