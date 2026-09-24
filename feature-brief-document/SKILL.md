---
name: feature-brief-document
description: Create or revise a Feature Brief in .workflow/features while Shape develops feature behaviour, stories, and acceptance criteria.
---

# Feature Brief document

Shape owns one Feature Brief for each substantial feature. The brief is working memory while Draft and the behavioural contract for Design while Ready. Design may correct non-material wording or links, with those changes included in Design acceptance. Material changes return to Shape.

## Create and locate

Read the related Backlog item, nearby briefs, and applicable Direction, Context, PDR, and ADR material. If the feature has no Backlog item, create one through `backlog-document` first. Use that item's stable ID as the feature ID. Store the brief at `.workflow/features/<feature-id>/brief.md`, such as `.workflow/features/B-0001/brief.md`. Link it from the Backlog item through `backlog-document`.

Before creating the file, check whether a brief for the feature exists elsewhere. Do not create a duplicate or migrate it in this skill. Ask for a separate migration when an existing brief is outside the canonical location.

Use this structure and omit optional sections when they add no value:

```markdown
# Feature title

Status: Draft
Feature ID: B-0001

## Goal

## Stories and acceptance

### S1: Short name

Story: Actor, situation, intent or action, and observable result.

Acceptance:

- Observable criterion.

## Feature-wide constraints and acceptance

## Scope

## Non-goals

## Related records

## Open questions and assumptions
```

Keep `Status: Draft` or `Status: Ready` near the title. Create a brief as Draft. Shape changes it to Ready only after explicit user agreement and a readiness review. If later evidence requires a material contract change, return it to Shape. Set Draft before changing behaviour, scope, stories, or acceptance criteria. Do not present a Draft brief as accepted behaviour.

## Content and acceptance

State the goal and intended value. Each story identifies an actor, situation, intent or action, and observable result. Put criteria under each story so their trace is clear. Put criteria that span stories under a named feature-wide constraint. Every story needs acceptance coverage. Cover relevant failure and boundary behaviour, permissions, persistence, lifecycle, and compatibility where observable.

State scope and non-goals. Link neighbouring features and shared Direction, Context, PDR, or ADR material when they constrain this feature. Record unresolved questions and unverified assumptions in Draft, clearly marked as such. Remove resolved questions and superseded wording instead of retaining a discussion history.

Ready requires one coherent vertical slice, agreed behaviour and boundaries, acceptance coverage, intentional scope and non-goals, and linked shared decisions. No open question may materially change the feature. A safely deferred assumption must leave the feature contract clear.

Do not include internal APIs, modules, schemas, classes, libraries, implementation plans, test code, copied shared rules, or speculative future behaviour.

## Size and validation

Aim for 500–900 words. The hard limit is 1,500 words per brief. Near that limit, remove copied decisions, history, and implementation detail. Split unrelated behaviour into another feature and update the Backlog relationship.

Use `concise-prose` and run `prose-check` when available. Install `workflow-document-check` alongside this skill and run it after edits. Check status, feature identity, story coverage, criterion trace, links, and unresolved material questions before finishing.
