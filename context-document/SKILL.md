---
name: context-document
description: Record agreed project-specific concepts in .workflow/context.md. Use when a collaborative workflow resolves terminology that must remain stable across features or fresh contexts.
---

# Context document

Context records the project's agreed language. It is authoritative for the
meaning of defined terms, not for project direction, feature behaviour, or
architecture. A code or document scan can suggest terms; it cannot authorize
an entry. The collaborative workflow and user establish the canonical meaning.
This skill records it.

## Check the language

Read `.workflow/context.md` first when it exists. Scan material that uses the
candidate term. Find competing names for one concept or one name used for
different concepts. Return unresolved ambiguity to the owning workflow.
Do not choose a canonical term or meaning silently.

Add an entry only when the concept is project-specific and needs one stable
meaning across features, documents, code, or fresh contexts. Reject ordinary
programming and framework vocabulary. Do not add a term only to satisfy an
STE or prose check. Create `.workflow/context.md` when the first term qualifies.
If a copy exists elsewhere, do not create a duplicate or migrate it here.

## Record the agreement

Use one short entry per concept:

```markdown
# Context

## Canonical term

- Meaning: One or two sentences that define the project concept.
- STE class: Technical name.
- Forms: Approved forms, when needed.
- Avoid: Misleading synonyms, when needed.
- Distinguish from: Related concept and its difference, when needed.
```

The heading gives the canonical spelling. Write one STE-compatible definition
that gives the term one project meaning. Keep meaningful distinctions and
approved forms explicit. Confirm the spelling, meaning, and STE class with the
user through the owning workflow. Omit optional fields
with no value. Link to related entries or records when a definition depends on
them.

Revise a definition when the user changes the agreed meaning. Check affected
uses in project documents and code. Route a behavioural change to a PDR or
Feature Brief, and an architectural change to an ADR; do not hide either in
Context. Do not add conversation history or generic project documentation.

Use `concise-prose` and `prose-check` when available. Check that each entry has
user-agreed meaning and no unresolved synonym or overloaded use.
