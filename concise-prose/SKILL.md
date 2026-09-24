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

For project files, `prose-check` derives approved technical terms from
`.workflow/context.md` and combines them with its separate shared vocabulary.
Use `--project-root` for standard input or files outside the project tree.
The Python environment that runs `prose-check` needs PyYAML for this derivation.

Do not add glossary entries merely to silence findings.
When fixing an error, make the smallest useful change.
Do not expand text only to satisfy a linter.
