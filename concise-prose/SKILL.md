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

After writing or substantially editing prose, run `prose-check` on edited Markdown files or pass other authored
prose on standard input. It checks STE100 first and then applies Vale's project
style rules if STE100 passes. Fix findings without changing technical meaning;
report a conflict if no safe correction exists.

For project files, `prose-check` combines shared vocabulary with two optional
project sources. `.workflow/context.md` defines agreed project concepts.
`.workflow/ste-glossary.json` approves domain words that do not need a project
definition. Add terms under `technical_nouns` or `technical_verbs`. Each list
accepts a word or an object with `word` and optional `inflections`. Keep
meanings and feature behavior out of the glossary. Use `--project-root` for
standard input or files outside the project tree. The combined vocabulary is
JSON, which STE100 accepts as YAML. The derivation uses only the Python
standard library.

When STE100 reports unknown words, collect all distinct words before editing
prose. Use `prose-check --vocabulary-report '.workflow/**/*.md'` to count findings
across files. Classify each word:

- Add established workflow or software terms to shared vocabulary when that
  source is available. Otherwise, report the proposed addition.
- Add established project or domain terms to `.workflow/ste-glossary.json`.
- Add project-specific concepts to Context only after the user agrees on their
  canonical meaning.
- Rewrite prose that uses unnecessary non-STE words.

Do not add entries merely to silence findings. Treat a large group of unknown
words as missing vocabulary first. Do not repeatedly rewrite sentences around
an established technical or domain term. Rewrite only the remaining prose,
then run `prose-check` again. Make the smallest useful change.
