# Workflow documents

Status: Draft

These guides define the durable project documents used by Mike's workflow.
They describe ownership, authority, lifecycle, required content, and exclusions.

## Document set

| Document | Skill | Kind | Created or maintained by | Authority |
| --- | --- | --- | --- | --- |
| [Direction](direction.md) | `direction-document` | Required singleton | Direction | Intended project end state |
| [Backlog](backlog.md) | `backlog-document` | Required singleton | Direction and Shape | Candidate work and relationships, not requirements |
| [Feature Brief](feature-brief.md) | `feature-brief-document` | Repeatable | Shape | Accepted feature behaviour only when ready |
| [Context](context.md) | `context-document` | Optional singleton | The collaborative step that resolves a stable term | Project terminology |
| [PDR](pdr.md) | `pdr-document` | Repeatable and created only when needed | Direction and Shape | Product or behavioural decision within its stated scope |
| [ADR](adr.md) | `adr-document` | Repeatable and created only when needed | Shape and Design | Architectural decision within its stated scope |
| [Acceptance Report](acceptance-report.md) | `acceptance-report-document` | One per Acceptance pass | Acceptance, then the responsible workflow steps and user | Evaluated findings, user guidance, and their current disposition |

## Document skills

Each durable document type has one document-specific skill. A workflow skill
must invoke it whenever the workflow creates or changes that document, including
small updates.

Each document skill defines:

- when to create and update the document;
- which workflow steps may change it;
- what the document must and must not contain;
- its required structure;
- its authority and lifecycle states;
- its links to related documents;
- its directory and file-naming rules;
- how to handle obsolete information; and
- the writing and validation skills to use.

The workflow skill remains responsible for the work and for deciding why the
document must change. The document skill governs how to make that change.

## Project document locations

Store durable workflow documents under `.workflow/` at the project root.
This directory contains project knowledge, not the workflow controller's
runtime state.

| Document | Location |
| --- | --- |
| Direction | `.workflow/direction.md` |
| Backlog | `.workflow/backlog.md` |
| Context | `.workflow/context.md` |
| Feature Brief | `.workflow/features/<feature-id>/brief.md` |
| Acceptance Report | Beside its Feature Brief, with its date and short Git SHA in the filename |
| PDR | `.workflow/decisions/pdr/` |
| ADR | `.workflow/decisions/adr/` |

Each document skill defines the filename rules for its repeatable documents.
Use one stable feature ID for the Backlog item and its Feature Brief folder.
The skills do not migrate documents from other locations. If a document exists
outside `.workflow/` and the canonical file is absent, ask for a separate
migration before creating another copy.

## Common rules

- Give durable knowledge one canonical home and link to it elsewhere.
- Do not copy shared rules into several documents.
- Distinguish draft working material from accepted content.
- Rewrite current-state documents as understanding changes; do not append a
  conversation history.
- Keep decision records as historical records. Supersede them explicitly rather
  than rewriting why an earlier decision was made.
- Keep documents short enough for a fresh context to load selectively.
- Preserve links from every affected Feature Brief to shared Direction, PDR,
  ADR, or Context material needed to understand it.

## Outside this taxonomy

Research is supporting material, not one document type. Code and tests are
implementation artifacts. Workflow and pause state belong to the workflow
controller. Conversations are disposable once durable knowledge reaches its
canonical home.
