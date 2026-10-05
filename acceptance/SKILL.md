---
name: acceptance
description: Assess Review findings against agreed feature intent and report blockers, decisions, and evidence gaps for the user's acceptance decision. Keep implementation and durable documents unchanged.
---

# Acceptance

Acceptance is a read-only decision and reporting step after Review. Answer:
Given the agreed feature and the evidence produced by Review, what should the
user know before deciding whether this feature is done?

Review investigates the implementation, runs checks, uses specialists, and
collects evidence in a temporary report. Acceptance evaluates that evidence
against agreed intent and presents a recommendation. The user or subsequent
workflow decides what to fix, defer, clarify, or accept.

## Read the handoff and agreed intent

Start with the Review report at
`.workflow/review/<feature-id>-<implementation-sha>.md` and the Feature Brief.
Confirm that feature ID and Implementation SHA match both the user's request
and the report.
Use relevant PDRs, ADRs, Direction, and Context documents when needed to
interpret a finding. The Design commit marks the implementation diff boundary;
it does not override durable intent.

Assess the reviewed Implementation revision. Report a missing or mismatched
handoff as an evidence gap. Do not substitute findings from another revision
or assume they apply to later changes. Any focused code inspection or check
must use the reviewed revision without disturbing the working tree.

## Assess retained candidates

Assess every retained Review candidate using its expected and observed
behaviour, evidence, consequence, preliminary severity, and uncertainty.
Preserve Review's candidate references; assign stable references if absent.
Relate each candidate to its governing story, acceptance criterion, PDR,
ADR, or other durable constraint where relevant.

Use the evidence already collected when it supports a disposition. Inspect
code or run a focused, read-only check only when a material uncertainty affects
the acceptance decision. Do not independently reproduce every candidate,
systematically walk the implementation, or repeat Review investigations.

Record one concise disposition for each candidate:

| Disposition | Meaning |
| --- | --- |
| Likely blocking problem | Evidence indicates a problem that prevents satisfying the agreed contract or materially undermines confidence in completion. |
| Non-blocking problem | Evidence indicates a problem whose consequence does not prevent acceptance under the agreed contract. |
| Likely acceptable | Evidence indicates that the observed behaviour satisfies agreed intent. |
| Outside feature scope | The concern falls outside this feature's agreed scope and applicable constraints. |
| Requires user/product decision | Ambiguous or conflicting intent requires a product, design, or user decision. |
| Insufficient evidence to decide | Material uncertainty prevents a supported disposition. |

Explain the consequence for acceptance and any remaining uncertainty. Review
severity is input, not the decision by itself. An unmet agreed story, criterion,
or applicable constraint indicates a blocker; deferral alone does not waive
the contract. Explain why a problem appears non-blocking. Missing evidence
does not establish acceptable behaviour.

Do not search for additional defects or perform another broad review. If a new
problem becomes obvious while evaluating a candidate, include it in the report
with its source and uncertainty. Do not broaden the investigation around it.

## Assess coverage gaps

Read Review's failed or incomplete checks and missing specialist coverage.
Determine whether each important gap materially prevents an acceptance
decision. Identify which stories, criteria, or constraints depend on that
evidence. A missing check is not automatically blocking; explain whether
available evidence is sufficient and why.

A focused check may clarify a material uncertainty using existing tooling.
Do not provision tooling, construct test infrastructure, or spend substantial
effort closing evidence gaps. Report an important gap that prevents a decision
and identify the investigation needed from a subsequent workflow. Do not rerun
all checks or create a new coverage audit.

## Preserve the decision boundary

Report confirmed problems to the user. Do not modify implementation code or
tests, add regression tests, commit fixes, run a fix/test/reverify loop, or
cherry-pick or port fixes between revisions. Acceptance does not complete the
feature itself.

The Acceptance report is the normal artifact. Keep Feature Briefs, PDRs, ADRs,
Direction, Context, and Backlog unchanged. Report conflicts between durable
documents instead of resolving them. Recommend the owning workflow for any
needed clarification or change.

Do not set the Feature Brief to Accepted automatically, including when the
recommendation is favourable. Unresolved material findings require the user's
final call. Any later status update or durable document change belongs to the
subsequent workflow after the user's decision. Preserve the Review report and
its evidence links; do not transfer evidence into other documents or delete
the handoff during Acceptance.

## Produce the user report

Write one concise, human-readable report at
`.workflow/features/<feature-id>/acceptance-<YYYY-MM-DD>-<implementation-sha>.md`.
Reuse it when resuming the same assessment. Keep it under 800 words. Link the
Review report and relevant contract sources rather than copying technical
investigations or creating a second specification.

Include these sections in order. State `None` where a section has no items:

1. **Feature and reviewed Implementation revision:** Feature ID, title, SHA,
   and links to the Feature Brief and Review report.
2. **Overall assessment:** Recommend acceptance, implementation follow-up,
   a user decision, or more investigation, with a brief rationale.
3. **Blocking findings:** Candidate references, dispositions, contract links,
   and concise consequences.
4. **Non-blocking findings:** Candidate references, dispositions, and reasons
   they do not prevent acceptance.
5. **Findings that appear acceptable or outside scope:** Candidate references,
   dispositions, and brief reasons.
6. **Decisions required from the user:** Unresolved intent or document conflicts,
   affected candidates, and the choice needed.
7. **Important evidence gaps:** Candidates with insufficient evidence,
   incomplete coverage, and how uncertainty affects the decision.
8. **Recommendation for what happens next:** Accept the feature, send specific
   findings back for implementation, settle a product/design decision, or
   request a bounded investigation. Name specific findings and the workflow.

Stop once retained candidates have dispositions and material decisions and
gaps are reported. Uncertainty is a valid report outcome, not a reason to
continue investigating indefinitely.

Apply `concise-prose` and run `workflow-document-check` on the Acceptance
report. Present the overall assessment, key blockers or decisions, and report
link to the user. Make clear that the recommendation awaits the user's
acceptance decision. Do not claim the feature is finished while material
findings remain unresolved.
