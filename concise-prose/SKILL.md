---
name: concise-prose
description: Write and review concise prose across documentation, source comments, and commit messages. Use STE100 for all authored prose and run prose-check after writing.
---

# Concise prose

Use this skill when writing or substantially editing prose, including Markdown
documentation, design documents, specifications, README and AGENTS files,
source documentation comments, and commit messages. Document-specific skills
decide what information belongs in each artifact.

Before writing, read and follow [ste100/SKILL.md](ste100/SKILL.md). All authored
prose uses STE100. Preserve verbatim material as-is: code, command output,
protocol strings, identifiers, quoted external text, and exact product or API
names where rewriting would be incorrect.

Optimize for information density.
Prefer deleting redundant or unnecessary text over rewriting it. Preserve useful
technical information and its intended meaning.
Avoid repeating information already stated in nearby prose.
State behavior directly.
Avoid introductory prose, summaries of the immediately preceding text, and conversational filler.

After writing or substantially editing prose, run `prose-check` on edited Markdown files.
Pass other authored prose on standard input. The command checks STE100 first.
When STE100 passes, it runs Vale. Treat findings as work to fix and rerun the
checker. Stop when the checked prose passes. Ask the user only when a specific
semantic decision prevents a safe fix.

For project files, `prose-check` combines three vocabulary sources:

- `shared-terms.json`: common software engineering and workflow language that
  is broadly reusable across projects.
- `.workflow/ste-glossary.json`: intentional project or domain language without
  a special canonical project meaning.
- `.workflow/context.md`: project concepts whose meaning must remain stable
  and explicit across contexts.

Add glossary terms under `technical_nouns` or `technical_verbs`. Each list
accepts a word or an object with `word` and optional `inflections`. Keep
meanings and feature behavior out of the glossary. A word does not need a
Context definition merely because STE100 does not know it. Use `--project-root`
for standard input or files outside the project tree.

When STE100 reports unknown words, collect all distinct words before editing
prose. Use `prose-check --vocabulary-report '.workflow/**/*.md'` to count findings
across files. Classify the words, then make one vocabulary or rewrite pass:

- Add common engineering or workflow terms to `shared-terms.json` when they
  are broadly reusable across projects.
- Add intentional project or domain terms to `.workflow/ste-glossary.json`.
- Add a term to Context only when it has an agreed canonical project meaning
  that must stay stable across contexts.
- Rewrite prose only when the unknown word is unnecessary or a clearer
  approved word exists.

Add a vocabulary term when the prose uses it intentionally and replacement
would reduce precision, clarity, or consistency. Repeated use across project
documents is strong evidence for project vocabulary. Prefer vocabulary
maintenance over awkward rewrites around legitimate technical terms.

Run `prose-check` again after each pass. Continue until STE100 passes. Then
fix Vale findings and rerun the checker. Do not respond to a large lint result
with only a list or summary. Report findings only when a semantic conflict
prevents an automatic fix.
