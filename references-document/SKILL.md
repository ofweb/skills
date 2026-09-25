---
name: references-document
description: Keep relevant external links and short relevance notes in a project's .workflow/references.md during Direction discussion.
---

# References document

Direction owns one optional `.workflow/references.md`. Create it when the first
relevant external link appears. Check for an existing references document
elsewhere before creating it. Do not create a duplicate or migrate a file in
this skill. Ask for a separate migration when needed.

Record relevant links supplied by the user or found during investigation.
Preserve a useful user link during the discussion even when its effect on
Direction is not yet known. Do not wait until the session ends. Read a source
before claiming that it supports a conclusion. If it has not been checked,
mark the relevant claim as unverified.

Use one entry per external source or closely related source set. Preserve the
source URLs and give the entry a clear title.
State why it may matter to the project's goal, a Direction topic, or an open
question. Link to the relevant Direction document when that helps navigation.
Use this compact form:

```markdown
# External references

## Source title

- Link: [Source title](https://example.com/source)
- Relevance: Short reason this source matters.
- Related: [Direction topic](direction/topic.md), when useful.
- Unverified: Claim or implication that still needs checking, when relevant.
```

The register is an index of evidence, not authority for product behaviour or
the intended end state. Direction documents and PDRs own the conclusions they
draw from sources. Link to a source instead of copying long passages or a
research report into the register.

Merge duplicate URLs and update the relevance note as understanding changes.
Do not remove a user-supplied link merely because its product implication is
unresolved. Remove an entry when it is no longer relevant, and update affected
links. Group entries by topic when that helps navigation. Keep each entry to a
few useful sentences. The register has no whole-file word limit.

Use `concise-prose` and run `prose-check` when available. Before finishing,
check that every entry has a working link, a reason to retain it, and clear
uncertainty where needed.
