# Decision

Status: Draft

## Purpose

Decision is a formal interruption for a high-impact question that must stop the
current work. It gives the user and Mike a focused context in which to examine
the issue, challenge assumptions, gather evidence, and determine what should
happen next.

Decision is not a delivery stage or a general discussion technique. Direction,
Shape, and Design handle ordinary collaborative questions in their own
contexts. Implementation handles local choices already constrained by accepted
behaviour and architecture.

## Responsibilities

Decision:

- isolates one consequential uncertainty;
- explains why the issue needs attention now;
- preserves the interrupted work's minimal return state;
- keeps judgement with the user rather than recommending an answer;
- investigates facts that could change the discussion;
- challenges current and inherited assumptions;
- allows uncertainty to remain when evidence is missing;
- persists every durable outcome before its context is cleared; and
- returns or reroutes the workflow after the interruption.

Decision does not:

- present generated options or recommendations;
- decide a product or architectural policy silently;
- interrupt work for cheap, local, reversible choices;
- preserve a transcript of the discussion;
- create an ADR or PDR merely because Decision ran; or
- assume that the interrupted work should always resume unchanged.

## Invocation threshold

Use Decision only when both conditions hold:

1. The question has high impact. If Mike chose alone and the user later
   disagreed, observable behaviour, architecture, ownership, persistence,
   protocol, lifecycle, or substantial work would need reconsideration.
2. Continuing the current work would implicitly settle the question or make
   later correction materially harder.

Examples include an invalid accepted contract, an unresolved ownership or
lifecycle boundary, new evidence against a durable decision, or a missing
product rule that blocks implementation.

Do not invoke Decision for naming, private helper structure, routine debugging,
or other choices that are constrained, reversible, and local.

## Invitation

Mike raises the interruption in the current conversation. It identifies:

- the exact question;
- the evidence or observation that exposed it;
- why the question is consequential; and
- why it needs attention now.

For example:

> I think we need to make a decision about ownership of reconnect state. The
> accepted lifecycle does not assign that responsibility, and implementation
> cannot continue without choosing it implicitly.

Mike then waits for the user's natural response. It does not present buttons,
an option list, a recommended action, or a suggested answer.

## Interpreting the response

The workflow interprets the user's response by meaning rather than requiring a
command syntax.

### Enter now

When the user agrees that the question needs attention now, the workflow:

1. creates a compact Decision Request;
2. saves minimal pause state for the interrupted work;
3. lets the current turn finish;
4. starts Decision in a fresh context; and
5. begins from the recorded question and linked evidence.

### Postpone

Postponement means the question is valid but another concern deserves attention
first. The user's reason is part of the postponement. Examples include finishing
the current topic before switching or assigning the question to another
feature.

The workflow does not switch context. It:

- records the unresolved question, importance, and postponement reason in the
  Feature Brief, Backlog, Direction document, or other artifact that owns it;
- records any return condition or feature named by the user;
- adds a queue entry that links to the canonical record instead of copying it;
- continues the current work; and
- avoids repeatedly raising the question before its return condition or
  dependency makes it relevant again.

### Do not enter

The user may explain that the issue is not consequential, is already settled,
rests on a false premise, or does not belong in the current work. Mike updates
its understanding and continues when possible.

Preserve the explanation only when it changes durable project knowledge. Do not
create a rejection log for every declined interruption.

## Decision Request and pause state

The Decision Request tells a fresh context what to discuss:

- the exact question;
- why it matters now;
- evidence that triggered the interruption;
- the active feature and workflow responsibility;
- the work affected or blocked;
- links to the minimum canonical artifacts; and
- the expected return point if the workflow can resume.

Pause state preserves only what the workflow needs to restore the interrupted
responsibility. It may include the active phase, feature, current operation,
verified file or test locations, and intended resume point.

Neither artifact is a conversation summary, architecture tour, evidence dump,
or durable project decision. The workflow controller owns their format and
lifecycle.

## Operating model

### 1. Reconstruct the question

Read the Decision Request, pause state, and linked canonical artifacts. Inspect
repository evidence when it can verify the premise. Do not import the previous
conversation into the new context.

### 2. Discuss one consequential point at a time

Mike states evidence, exposes assumptions, identifies contradictions, and asks
focused questions that require the user to reason about the issue.

Mike does not lead with a recommendation, generate an option matrix, or steer
the user toward a preferred answer. It may use a concrete counterexample or
consequence to challenge an assumption.

Earlier effort gives a direction no special authority. New evidence may reopen
a prior choice when it invalidates the premise on which that choice depended.

### 3. Investigate when knowledge is missing

Decision may inspect the repository, research external facts, run a small
experiment, or consult a remote model when a specific unresolved premise
requires it.

Remote consultation asks for evidence, falsification, or a missing consequence.
It does not ask the remote model to make the decision. Remote output returns to
the user discussion as untrusted input that Mike verifies where practical.

### 4. Establish the outcome

Decision succeeds when the uncertainty is understood well enough to know what
happens next. The outcome may be:

- a resolved choice;
- a corrected premise;
- a defined investigation or experiment;
- a return to Direction, Shape, or Design;
- a safe resumption of the interrupted work; or
- an explicitly preserved question that still cannot be answered.

Do not manufacture certainty to close the interruption.

### 5. Persist durable knowledge

Before leaving Decision, ask what must survive the context reset and route it to
its canonical home:

- project destination → [Direction document](../documents/direction.md);
- future work or reassigned question → [Backlog](../documents/backlog.md);
- feature-specific behaviour or open question →
  [Feature Brief](../documents/feature-brief.md);
- durable product or behavioural decision → [PDR](../documents/pdr.md);
- durable architectural decision → [ADR](../documents/adr.md);
- stable terminology → [Context](../documents/context.md); and
- local reversible judgement → no durable document.

Decision may write or update the owning document before the context is cleared.
It follows that document's guide and does not take permanent ownership from
Direction, Shape, or Design.

When the outcome changes accepted behaviour or architecture, route through the
collaborative step that owns that contract before autonomous work resumes.

### 6. Return or reroute

Verify that the durable outcome and next workflow destination are recorded.
Then request a controller-owned transition into a fresh context.

Resume from the saved point only when the outcome preserves the interrupted
work's assumptions. Otherwise discard the stale return path and route to the
responsible collaborative step.

## Completion

Decision is complete when:

- the triggering uncertainty has a clear outcome or next investigation;
- durable knowledge has reached its canonical home;
- affected contracts and queued questions are updated;
- stale pause or queue state is removed or redirected;
- the next workflow responsibility is explicit; and
- the controller can start that responsibility without the Decision
  conversation.

The Decision context is cleared after these conditions pass.

## Failure behaviour

- If evidence is missing, preserve the question and define how to obtain the
  evidence.
- If documents conflict, do not choose one silently; route the conflict to its
  owner.
- If the user postpones, preserve the reason and continue without switching
  context.
- If the user rejects the interruption, update the premise and continue when
  safe.
- If the outcome invalidates the saved return point, reroute instead of forcing
  a resume.
- If no canonical document can hold important knowledge, do not clear the
  context until ownership is resolved.

## Open questions

The workflow controller still needs to define:

- the Decision Request and pause-state schemas;
- how queued decisions are indexed without duplicating their canonical text;
- how return conditions surface a postponed question;
- transition validation before entering and leaving Decision; and
- how document-specific writing procedures are invoked from Decision.
