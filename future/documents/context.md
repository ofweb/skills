# Context document

Status: Draft

## Purpose

The Context document records the project's agreed language. It defines stable
project-specific concepts for the user, fresh agent contexts, documentation,
and code where relevant.

## Ownership and cardinality

- Context is optional and created lazily when the first durable term needs a
  canonical definition.
- Store it at `.workflow/context.md` from the project root.
- Use one document unless the project has genuinely separate domain languages.
- The collaborative workflow step that resolves or changes a term updates it.
- The user agrees each concept, canonical term, meaning, and STE vocabulary
  definition.
- Autonomous work must not invent or redefine project terminology silently.
- Repository and document scans may find candidate terms, but discovery does
  not authorize adding them.

## Contains

- project-specific terms;
- concise definitions;
- important distinctions between similar concepts;
- preferred vocabulary and misleading synonyms to avoid; and
- stable relationships between concepts when a definition needs them.

Definitions should state what a concept is in one or two sentences. Include
only terms whose meaning is specific to the project.

Read existing entries before adding or changing a term. Surface competing
words for one concept and overloaded words for different concepts to the
collaborative workflow. That workflow resolves the meaning with the user;
Context records the agreed result.

Each concept also provides the vocabulary information needed by prose checks:

- its canonical spelling;
- its ASD-STE100 classification as a technical name or technical verb;
- approved forms when plurals, tense, or another form could be ambiguous; and
- a short STE-compatible definition that gives the term one project meaning.

The Context document is the canonical source for this vocabulary.
`prose-check` may derive checker input from its entries but must not maintain a
separate project glossary.

## Concept qualification

Add a concept only when all of these conditions hold:

- its meaning or allowed use is specific to the project;
- the meaning must remain stable across features, documents, or fresh
  contexts;
- a canonical definition prevents real ambiguity, drift, or duplicate
  concepts;
- the concept has a clear scope and one intended project meaning; and
- the user agrees the concept and its definition.

A checker finding does not qualify a term. When ASD-STE100 rejects an unknown
project term, Mike asks whether the term represents a durable project concept.
It does not add the term merely to make prose validation pass.

## Does not contain

- project direction or future capabilities;
- feature requirements or acceptance criteria;
- architecture or implementation details;
- ADR or PDR rationale;
- workflow state, progress, or handoff information;
- general programming terminology; or
- framework and tool terminology used with its ordinary external meaning;
- transient discussion vocabulary, one-off labels, and local symbol names;
- terms added only to suppress a prose-check finding; or
- a narrative introduction to the whole codebase.

## Authority and maintenance

Context is authoritative only for terminology. Code, Feature Briefs, and
decision records link to it when a term's precise meaning matters.

The future `context-document` skill applies the concept-qualification
rules, asks the user to establish the canonical meaning, and writes the Context
entry. Prose validation reads approved entries but cannot create or change
them.

Update a definition when the project meaning changes. If that change also
changes product behaviour, record a PDR. If it changes architecture, record an
ADR. Do not hide either decision inside the glossary.
