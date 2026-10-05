---
name: workflow-document-check
description: Check workflow Markdown, Feature Brief structure and links, and document word limits. Use after changing .workflow documents.
---

# Workflow document check

Run `python scripts/check_workflow_docs.py <project-root>` from this skill
directory. The command also accepts no path and then checks the current
directory. Python 3.10 or newer is required. The skill includes its Markdown packages. The command prints stable rule IDs, file
paths relative to the project, and line numbers. It exits with status 1
for errors, status 2 for a tool failure, and status 0 when it finds only
warnings or no findings.

The checker uses `markdown-it-py` to parse Markdown and an anchor plugin
to find heading IDs. It checks local links, Feature Brief structure,
backlog relationships, and all existing hard word limits. Read
[rules.md](references/rules.md) when a finding needs interpretation.

A Draft Feature Brief must have valid structure and links. Missing
content is a warning. A Feature Brief with status Ready, Designed, Implemented,
Reviewed, or Accepted must also be mechanically complete. Semantic readiness
and stage completion remain user and reviewer decisions.
The checker cannot decide whether scope, acceptance coverage, or open
questions are good enough.

The checker counts whitespace-separated words in Markdown source,
including headings and link text. A hard-limit error calls for pruning
or a clearer document boundary. Do not fill documents to their hard
limits.

To maintain the validator, edit `scripts/validate.py`, run
`python scripts/build_bundle.py`, then run
`python -m unittest discover -s tests` from this skill directory.
The tests fail if the bundled validator differs from the source.
