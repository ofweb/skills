---
name: workflow-document-check
description: Check workflow Markdown, Feature Brief structure and links, and document word limits. Use after changing .workflow documents.
---

# Workflow document check

Install dependencies once in this skill directory with `npm ci`. Run
`python scripts/check_workflow_docs.py <project-root>` from this skill
directory. The command also accepts no path and then checks the current
directory. Node.js is required. The command prints stable rule IDs, file
paths relative to the project, and line numbers. It exits with status 1
for errors, status 2 for a tool failure, and status 0 when it finds only
warnings or no findings.

The checker uses `remark` to parse Markdown and `remark-validate-links`
to check local files and anchors. It checks Feature Brief structure,
backlog relationships, and all existing hard word limits. Read
[rules.md](references/rules.md) when a finding needs interpretation.

A Draft Feature Brief must have valid structure and links. Missing
content is a warning. A Ready Feature Brief must also be mechanically
complete. Semantic readiness remains a user and reviewer decision.
The checker cannot decide whether scope, acceptance coverage, or open
questions are good enough.

The checker counts whitespace-separated words in Markdown source,
including headings and link text. A hard-limit error calls for pruning
or a clearer document boundary. Do not fill documents to their hard
limits.
