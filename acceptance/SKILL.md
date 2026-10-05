---
name: acceptance
description: Complete one feature after Review by independently verifying retained candidates, fixing defects within agreed intent, resolving evidence gaps, and recording the final acceptance outcome.
---

# Acceptance

Acceptance is the final feature-completion step after Review. It owns the
decision that the feature is done. Review supplies broad inspection and
evidence-backed candidates; Acceptance verifies those candidates and closes
the remaining gaps. Do not repeat Review from scratch. Acceptance may change
implementation code and tests. Review must not.

## Establish intent and the snapshot

Read the Feature Brief, applicable Direction and Context documents, linked
PDRs and ADRs, the immutable Implementation commit, and the temporary report
at `.workflow/review/<feature-id>-<implementation-sha>.md`. Confirm that the
feature ID and commit match the report. The Design commit marks the diff
boundary; it does not override durable intent.

Start from the reviewed implementation. Preserve Review's brief status update
and isolate unrelated working-tree changes before fixing code. Keep the
Implementation commit unchanged. Track Acceptance fixes separately and
evaluate the resulting revision. When resuming, read the existing acceptance
record and retained fixes rather than resetting to the Implementation commit.

## Verify and classify candidates

Verify every retained candidate independently. Read its governing contract and
affected code, reproduce the behaviour where practical, and inspect or run
tests that distinguish expected from observed behaviour. Review's conclusion
and preliminary severity are leads, not proof.

Give each candidate a stable reference. Record its classification, evidence,
acceptance consequence, and disposition:

| Classification | Meaning |
| --- | --- |
| Confirmed defect | Implementation or test behaviour is wrong under settled intent. |
| Requirement violation | An explicit feature requirement or durable constraint is unmet. |
| Acceptable behaviour | Observed behaviour satisfies the agreed contract. |
| Outside feature scope | The concern does not belong to this feature or its affected paths. |
| Unresolved requirement ambiguity | Conflicting or unclear intent prevents a verdict. |
| Unverifiable with the available environment | Missing execution capability or evidence prevents verification. |

State what remains unknown instead of treating inability to reproduce as
acceptable behaviour. Reclassify when new evidence changes the verdict.
Verify newly discovered problems within the feature's affected paths too.

Decide whether each confirmed finding blocks acceptance from its effect on
stories, acceptance criteria, constraints, and confidence in the evidence.
Explain that decision; do not copy Review's severity mechanically. An unmet
agreed story, criterion, or applicable constraint blocks acceptance. Deferral
does not waive the contract. Other confirmed issues can remain non-blocking
when their consequences and reasons are explicit.

## Fix within agreed intent

Fix confirmed implementation defects and requirement violations when the
correction follows unambiguous, already-agreed behaviour and architecture.
Apply [simple-code](../simple-code/SKILL.md) to the correction. Keep changes
within the affected responsibilities and avoid unrelated cleanup.

Add or strengthen tests when needed to demonstrate the failure and prevent
regression. Confirm that the test detects the original defect where practical.
Fix the implementation, run focused tests and checks, then independently
re-evaluate the finding and affected behaviour. Continue this verify, fix,
test, and verify loop until no blocking implementation defects remain.
Straightforward defects normally belong in this loop.

Do not rewrite requirements or weaken tests to make a defect disappear. When
a correction requires interpreting ambiguous intent, choosing between
conflicting documents, or changing a product or architectural decision,
explain the evidence and the decision required. Recommend a next step and ask
the user to approve or change it through the owning workflow: Direction for
end-state decisions, Shape for feature behaviour, and Design for architecture.
Keep the affected correction and acceptance decision blocked until settled.
Continue independent work that does not depend on that decision.

After the decision, update canonical documents through their document skills
in the owning workflow. Re-evaluate affected findings against the agreed
contract. Material contract changes return through Shape; do not silently
preserve an obsolete readiness or acceptance claim.

## Establish sufficient evidence

Assess failed or incomplete Review checks and missing specialist coverage.
Identify which stories, criteria, or constraints depend on that evidence.
Fill important gaps with focused inspection, tests, or execution where
practical. A missing check or specialist is not automatically blocking; decide
whether available evidence supports a credible completion decision and record
the reason. Critical unverified behaviour prevents acceptance.

Use Review evidence that still applies to unchanged code. After fixes, rerun
checks that cover the changes and their integration effects, including
configured compile, test, lint, format, and prose checks. Broaden verification
when the change invalidates earlier evidence. Re-evaluate affected findings
and check for regressions introduced by the fixes. Do not start another broad
review merely because Acceptance changed code.

Before accepting, trace every agreed story, acceptance criterion, and
applicable constraint to sufficient evidence at the final code revision.
Passing checks or having no retained candidates alone does not establish
acceptance.

## Record the outcome and close the loop

Maintain one compact acceptance record at
`.workflow/features/<feature-id>/acceptance-<YYYY-MM-DD>-<implementation-sha>.md`.
Reuse it when resuming. Record the feature ID, reviewed Implementation SHA,
final verified code revision, outcome and rationale, candidate dispositions,
evidence and coverage gaps, and links to remaining issues or decisions. Keep
it under 800 words. Summarize evidence and link its canonical sources instead
of copying Review prose or keeping a second specification.

Commit verified code and test fixes, if any, and record the resulting revision.
Choose the outcome from the evidence:

| Outcome | Condition |
| --- | --- |
| Accepted | Blocking findings are resolved, remaining findings are explicitly non-blocking or deferred, and sufficient evidence shows that the agreed contract is satisfied. |
| Needs decision | Acceptance depends on an unresolved product, architecture, or requirement decision. |
| Cannot establish acceptance | Critical behaviour cannot be verified with the available environment or evidence. |

For Accepted, set the Feature Brief to Accepted through
`feature-brief-document`. For either other outcome, do not mark it Accepted;
record the exact decision or missing evidence and the next step. These
outcomes are acceptance decisions, not additional Feature Brief statuses.

Transfer information that should survive the workflow to its canonical home.
Keep agreed behaviour in the Brief, product decisions in PDRs, architecture in
ADRs, and project terminology in Context. Record non-blocking confirmed issues
in an existing issue record or the acceptance record, with consequence and
deferral rationale. Use Direction and `backlog-document` only for agreed
future features; do not turn internal repair tasks into Backlog items.
Record unresolved candidates and evidence gaps for resumption when acceptance
cannot finish. Do not invent decisions while transferring information.

Apply `concise-prose` and run `workflow-document-check` after document edits.
Verify that transferred information and links survive without the temporary
report, then delete that report. Preserve any untransferred evidence until it
has a durable home. Commit the final workflow state without unrelated changes.

## End-of-step report

State the outcome and its evidence. For Accepted, say that the feature is
finished. Name the verified code revision and final commit, summarize fixes
and checks, and link any non-blocking issues and the acceptance record. For
other outcomes, name the decision or evidence needed to continue and link the
record. Do not claim completion while either remains unresolved.
