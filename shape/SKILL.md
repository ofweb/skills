---
name: shape
description: Refine a Direction idea or Backlog item into small features, maintain draft Feature Briefs, and agree on observable behaviour before Design.
---

# Shape

Shape is a collaborative discussion about feature behaviour and boundaries. The user names the idea or related work to shape. Shape may prepare several related features, but it selects at most one ready Feature Brief for Design.

## Orient and bound the work

Read the relevant `.workflow/direction.md` sections, Backlog items, Feature Briefs, and linked decisions. Inspect repository behaviour before relying on claims about the current system. Investigate prior art when it can change expected behaviour or feature boundaries. Read only context relevant to the active question.

Identify the candidate feature or small related group under discussion. Shape related candidates together only while their boundaries or order need joint reasoning. Leave independent candidates for later rounds. Direction and Backlog wording supplies ideas, not accepted requirements.

## Explore behaviour

Build a current understanding of the feature with the user. Find inconsistencies, hidden assumptions, implied behaviour, and boundaries that may be simpler. Revise that understanding as the discussion changes. Keep one consequential issue active. Explore tightly coupled issues together when separating them hides a trade-off. Do not ask through a requirements checklist.

Reason before asking for the next product judgment. Investigate repository behaviour or prior art when evidence can settle a question. State supported factual conclusions clearly. Compare genuinely different approaches when useful. Challenge weak reasoning and explain the premise behind the challenge. Synthesize what is settled and name the remaining judgment before asking. Leave consequential product judgments to the user. Do not lead with a recommendation or an option menu.

Use concrete stories to examine the actor, situation, intent, and observable outcome. Examine successful behaviour, failures, permissions, persistence, lifecycle, compatibility, and safety when relevant. Use these as lenses, not a fixed question sequence. State scope and non-goals as understanding improves. Keep uncertain behaviour in Draft until the user resolves, verifies, removes, or safely defers it.

Prefer the smallest coherent feature with an independently observable outcome. Do not invent a system actor or story to make engineering work appear to be a feature. Put work without independent value in the Backlog as engineering work supporting another feature. Do not use Shape to choose internal APIs, modules, data structures, libraries, implementation plans, or test code.

## Maintain durable records

Update the affected documents during the discussion when a behaviour,
boundary, relationship, or important question becomes clear enough to
preserve. Make the edit before moving to another consequential issue, then
continue the discussion. Do not edit after every exploratory turn or defer all
updates until the end. Keep partial understanding in Draft and mark tentative
parts clearly.

Use `backlog-document` when candidate work, maturity, or durable relationships change. Create a Backlog item for a Direction idea before it needs a Feature Brief. A compact item is enough until stories, behaviour, boundaries, or open questions need a durable working record. Use `feature-brief-document` to create and update every Feature Brief touched during the discussion. Keep each draft current and mark tentative content and unverified assumptions.

Draft Feature Briefs are Shape's persistent working memory. Conversation is disposable. Do not create separate Shape notes, context dumps, or handoff documents. Keep stable relationships between future work in the Backlog.

Use `context-document` for agreed project terms and `pdr-document` for durable product decisions whose rationale matters beyond one feature. Use `adr-document` only when an architectural choice must be settled to establish feasibility, observable behaviour, or feature boundaries. Link each affected Feature Brief to shared decisions and constraints. If evidence challenges Direction or an existing decision, return the question to its owning workflow instead of silently changing it.

## Establish acceptance and readiness

Give every feature at least one user or system story. Give every story observable acceptance coverage. Trace each criterion to its story or a named feature-wide constraint. Include relevant failures and boundaries. Keep acceptance criteria about behaviour, not internal design or test implementation.

Review each brief for one coherent feature, agreed behaviour, explicit scope and non-goals, acceptance coverage, linked shared decisions, and material assumptions. Present unresolved concerns to the user. Set `Status: Ready` only after the user explicitly agrees that the brief is ready. File existence or complete-looking prose does not imply agreement.

If later evidence requires a material change to behaviour, scope, stories, or acceptance criteria, return the brief to Shape. Set `Status: Draft` before changing that contract. Update the Backlog with the resulting boundaries and durable relationships. Ready briefs that are not selected remain available for later work.

Select no more than one Ready brief as the next Design input. Do not send a Draft brief to Design to resolve a product question. A Shape session may end with only Backlog or Draft brief progress.

Until a workflow controller can clear context, use a manual transition. Save and check the durable documents. State the selected feature ID, Ready brief, and completed checks. If Shape left repository changes, tell the user to commit them before Design's clean-tree entry gate. Then tell the user to run `/clear` and start Design for that feature ID. Do not continue Design in the Shape context.
