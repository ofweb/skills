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
checker. Stop when the checked prose passes. Ask for the vocabulary review
below. Ask about other findings only when a semantic decision prevents a safe fix.

For project files, `prose-check` combines three vocabulary sources:

- `shared-terms.json`: common software engineering and workflow language that
  is broadly reusable across projects.
- `.workflow/ste-glossary.json`: intentional project or domain language without
  a special canonical project meaning.
- `.workflow/context.md`: project concepts whose meaning must remain stable
  and explicit across contexts.

`shared-terms.json` belongs to the `ofweb/skills` repository. When developing
this skill there, add reviewed, broadly reusable engineering and workflow terms
directly to that file. In a consuming project, treat the installed file as read-only.
Use the project's glossary for intentional local vocabulary and Context for
canonical project concepts. Do not edit the installed skill copy from a
consuming project. Suggest repeated local terms for promotion to shared
vocabulary when they could help many projects. Make and review that change in
`ofweb/skills` before it enters the common language profile.

Add glossary terms under `technical_nouns` or `technical_verbs`. Each list
accepts a word or an object with `word` and optional `inflections`. Keep
meanings and feature behavior out of the glossary. A word does not need a
Context definition merely because STE100 does not know it. Use `--project-root`
for standard input or files outside the project tree.

When STE100 reports unknown words, collect all distinct words before editing
prose. Use `prose-check --vocabulary-report '.workflow/**/*.md'` to count findings
across files. Search existing project documents when usage can help classify a
term. Classify every distinct unknown term as one of these:

- Shared vocabulary candidate: common engineering or workflow language.
- Project vocabulary candidate: intentional project or domain language.
- Context concept candidate: a project meaning that must stay stable.
- Ordinary prose to rewrite: an unnecessary term or one with a clearer approved word.
- Probable checker or document-structure finding: inspect the checker or Markdown extraction.

Rewrite ordinary prose without asking the user when meaning stays intact.
Investigate probable checker or document-structure findings. Run `prose-check`
again after each rewrite or tooling pass. When unknown vocabulary remains, do
not stop with the raw checker output.

Before adding vocabulary, present all candidate terms in one review group.
For each term, give its proposed source and a short reason. Include a short
example from the project when the classification is not clear. Do not present
the full lint output unless the user asks for it. Wait for the user's review
before adding vocabulary.

Apply accepted project terms to `.workflow/ste-glossary.json`. Add a Context
concept only after its canonical meaning is agreed. Change shared vocabulary
only in `ofweb/skills`, after review. Do not edit the installed copy from a
consuming project. Run `prose-check` again after each vocabulary pass.

Add a vocabulary term when the prose uses it intentionally and replacement
would reduce precision, clarity, or consistency. Repeated use across project
documents is strong evidence for project vocabulary. Prefer vocabulary
maintenance over awkward rewrites around legitimate technical terms.

Continue until STE100 passes. Then fix Vale findings and rerun the checker.
Treat large lint results as work to perform, not a report to summarize. Report
remaining findings only when a semantic conflict prevents a safe fix.
