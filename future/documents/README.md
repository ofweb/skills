# Workflow documents

Status: Draft

These guides define the durable project documents used by Mike's workflow.
They describe ownership, authority, lifecycle, required content, and exclusions.

## Document set

| Document | Skill | Kind | Created or maintained by | Authority |
| --- | --- | --- | --- | --- |
| [Direction](direction.md) | `direction-documentation` | Required singleton | Direction | Intended project end state |
| [Backlog](backlog.md) | `backlog-documentation` | Required singleton | Direction and Shape | Candidate work and relationships, not requirements |
| [Feature Brief](feature-brief.md) | `feature-brief-documentation` | Repeatable | Shape | Accepted feature behaviour only when ready |
| [Context](context.md) | `context-documentation` | Optional singleton | The collaborative step that resolves a stable term | Project terminology |
| [PDR](pdr.md) | `pdr-documentation` | Repeatable and created only when needed | Direction and Shape | Product or behavioural decision within its stated scope |
| [ADR](adr.md) | `adr-documentation` | Repeatable and created only when needed | Shape and Design | Architectural decision within its stated scope |
| [Acceptance Report](acceptance-report.md) | `acceptance-report-documentation` | One per Acceptance pass | Acceptance, then the responsible workflow steps and user | Evaluated findings, user guidance, and their current disposition |

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
