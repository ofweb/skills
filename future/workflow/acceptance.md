# Acceptance

Status: Draft

## Purpose

Acceptance evaluates the candidate findings produced by Review and determines
whether the feature is complete. It starts in a fresh context, independently
assesses each candidate, and involves the user only for verified issues worth
the user's attention.

Acceptance keeps an [Acceptance Report](../documents/acceptance-report.md)
beside the Feature Brief while verified findings need follow-up.

## Responsibilities

Acceptance:

- reconstructs the feature and reviewed revision from durable artifacts;
- evaluates whether each Review candidate deserves investigation;
- independently assesses impact and severity instead of trusting the
  specialist's preliminary judgement;
- verifies candidates selected for investigation;
- may group related candidates for remote verification under the
  remote-consultation skill's policy;
- organizes verified findings into underlying topics;
- discusses major topics first when user guidance is needed;
- records verified findings, user guidance, ownership, and current disposition
  in its report while findings require follow-up;
- examines every candidate worth the time before ending the pass;
- deletes the temporary Review report after transferring relevant evidence;
  and
- marks a feature complete without discussion when no verified issue deserves
  user attention.

Acceptance does not:

- expose every Review candidate to the user;
- trust a specialist's finding, impact, or severity without its own
  evaluation;
- recommend a response or suggest a solution;
- change code, feature behaviour, or accepted Design;
- impose an execution order on later workflow steps; or
- copy unresolved findings from an older Acceptance Report into a new one.

## Inputs

Acceptance reads:

- the ready [Feature Brief](../documents/feature-brief.md);
- the reviewed implementation revision and accepted Design;
- linked [Direction](../documents/direction.md),
  [Context](../documents/context.md), [PDR](../documents/pdr.md), and
  [ADR](../documents/adr.md) material;
- the temporary Review report;
- code, tests, and mechanical results needed to evaluate its candidates; and
- current Acceptance Reports when unresolved work refers to their findings.

Acceptance does not inherit the Review or Implementation conversations.

## Outputs and authority

An Acceptance pass creates an Acceptance Report when it retains findings that
need follow-up. The report names its date and reviewed Git revision. It does
not replace the Feature Brief or make a proposed change authoritative. A clean
pass leaves no lasting report.

Acceptance may:

- mark the feature complete when no finding requires user attention;
- record user-guided work for Shape, Design, Implementation, or another owner;
- leave the feature unfinished while that work remains unresolved; or
- record the user's decision to complete the feature despite remaining items.

The user chooses which workflow step should pick up recorded work first. Each
step determines dependencies and whether earlier work must be revisited when it
reads the report.

## Operating model

### 1. Reconstruct the acceptance target

Read the Feature Brief, reviewed revision, accepted Design, linked decisions,
and temporary Review report. Confirm that the report identifies the code
revision it examined.

### 2. Evaluate investigation value

Consider every candidate finding. Decide whether further investigation is
worth the attention it requires based on its relevance, plausible impact,
evidence quality, and investigation cost.

Candidates that do not justify investigation are omitted. They do not enter the
Acceptance Report or consume user attention.

### 3. Verify selected candidates

Independently verify every candidate selected for investigation. Reassess its
impact and severity from evidence rather than inheriting the specialist's
labels.

Acceptance may group related candidates in a remote request. The
remote-consultation skill controls grouping limits, retries, cooldowns,
capacity, model choice, and token accounting. Remote output is evidence, not a
decision or recommendation.

The exact local and experimental verification methods remain open. Acceptance
must not present a candidate as a defect merely because Review or a remote
model reported it.

### 4. Record retained findings

Create a report when the current pass retains findings. Use a filename such as:

```text
acceptance-2026-09-22-a1b2c3d.md
```

Record the full Git SHA inside the report. Store it in the same feature folder
as the Feature Brief.

Transfer the evidence needed for retained findings, then delete the temporary
Review report. Do not copy unresolved findings from earlier current reports.
They remain owned by their original reports. A clean pass can finish without
an Acceptance Report.

### 5. Discuss verified topics

Group related verified findings by their underlying topic. Begin with major
topics that may resolve or invalidate several findings. Present the problem,
evidence, impact, and affected behaviour or structure without recommending a
response.

Use the user's guidance to update the report after each topic. Continue until
every verified finding worth user attention has been discussed.

### 6. Route later work

Associate each required change with the workflow step that appears to own it.
Do not impose dependencies or execution order during Acceptance. After the
pass, the user chooses the step whose work is most pressing.

The receiving step reads the report, determines dependencies and stale
assumptions, and updates its items. It may complete, ignore, reassign, or remove
items that have become outdated or irrelevant. The user may update or remove
items at any time.

### 7. Determine feature status

Mark the feature complete without user discussion when no verified issue
deserves user attention and no earlier current report still requires work.
Remove earlier reports whose findings this pass resolved or invalidated.

When the report contains required changes, the Acceptance pass ends but the
feature remains unfinished. It may remain paused while the user prioritizes
other work. The user may later decide that the remaining work is not important
and mark the feature complete.

## Report lifecycle

Keep only reports with findings that still constrain current work. Update them
when their findings are worked on; remove them when the work is resolved,
outdated, or no longer relevant. Git preserves earlier passes.

A newer report does not carry older unresolved items forward. Date and Git SHA
identify what each retained report evaluated. Remove obsolete findings and
update affected links. Each report normally uses 250–500 words and must stay
within 800 words. Keep findings concise; do not retain review transcripts.

## Completion

An Acceptance pass is complete when:

- every Review candidate has received an investigation-value assessment;
- every selected candidate has been independently evaluated;
- verified findings have been organized into topics;
- every topic worth user attention has been discussed;
- any retained report records current findings and guidance;
- evidence for retained findings is preserved in that report;
- the temporary Review report is deleted; and
- the feature is marked complete or its unfinished status and available return
  steps are explicit.

Completing the pass does not complete a feature that still has required work.

## Failure behaviour

- Do not expose low-value or unverified candidates to the user.
- Preserve uncertainty when verification cannot establish a finding.
- Do not let remote analysis decide a finding or its disposition.
- Do not delete the Review report until required evidence is transferred.
- Do not mark the feature complete while required work remains unless the user
  explicitly closes it.
- Do not infer ordering among follow-up steps; let the step that picks up an
  item assess its dependencies.

## Open questions

The workflow still needs to define:

- the local and experimental verification methods available to Acceptance;
- the report schema and permitted status vocabulary;
- how a Feature Brief indexes several current Acceptance Reports;
- filename collision handling for repeated passes on one revision and date;
- how feature completion is represented in workflow state; and
- the exact return transition from a report item to each owning step.
