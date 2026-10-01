---
name: concise-prose
description: Write and review concise prose across documentation, source comments, and commit messages. Apply writing principles and run prose-check after writing.
---

# Concise prose

Use this skill when writing or substantially editing prose, including Markdown
documentation, design documents, specifications, README and AGENTS files,
source documentation comments, and commit messages. Document-specific skills
decide what information belongs in each artifact.

Apply these principles while writing:

- Prefer short, direct sentences.
- Prefer one idea or instruction per sentence.
- Prefer direct verbs and active voice.
- Prefer simple wording when it does not reduce precision.
- Consult CONTEXT.md for establisted project terms.
- Use one term consistently for one concept.
- Preserve established technical terminology.
- Preserve meaning over satisfying a prose rule.

Split a long sentence when it improves clarity. There is no fixed sentence
word limit or controlled vocabulary. Keep code, command output, protocol
strings, identifiers, quoted external text, and exact product or API names
verbatim where rewriting would be incorrect.

Prefer deleting redundant or unnecessary text over rewriting it. Preserve useful
technical information and its intended meaning. Avoid repeating nearby prose.
State behavior directly. Avoid introductory prose, summaries of the immediately
preceding text, and conversational filler.

After writing or substantially editing prose, run `prose-check` on edited
Markdown files. Pass other authored prose on standard input. The command runs
Vale to find mechanical prose problems using the bundled configuration and
styles. Fix useful findings and rerun until clean or until a finding would
require changing intended meaning. Preserve that meaning and explain any
remaining finding. Prose linting does not decide document content or require
vocabulary classification or approval.
