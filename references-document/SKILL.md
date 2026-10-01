---
name: references-document
description: Keep external sources with durable project value and short relevance notes in a project's .workflow/references.md.
---

# References document

Direction owns one optional `.workflow/references.md`. Create it when the first
source has durable project value. Check for an existing references document
elsewhere before creating it. Do not create a duplicate or migrate a file in
this skill. If a migration is needed, present the found path and required
canonical destination. Recommend a separate migration to keep one source
register. Ask the user to approve starting that migration or request changes.
Keep this file operation blocked until the migration is complete.

Record a source when it affects Direction, supports a decision, resolves an
important uncertainty, or is likely to help again. Do not record every source
inspected. Preserve a useful user link even when its effect on Direction is not
yet known. Read a source before claiming that it supports a conclusion. If it
has not been checked, mark the claim it supports as unverified.

Use one entry per external source or closely related source set. Preserve the
source URLs and give the entry a clear title.
State why it may matter to the project's goal, a Direction topic, or an open
question. Link to the Direction document that covers the topic when that helps
navigation.
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

Invoke `concise-prose` before writing or revising References. Apply its
principles and run `prose-check` as described there. Before finishing,
check that every entry has a working link, a reason to retain it, and clear
uncertainty where needed.
