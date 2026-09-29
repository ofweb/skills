# Workflow validation rules

The validator uses three layers. This release applies generic Markdown
checks to `.workflow` files. It applies workflow identity and content
rules to Feature Briefs and their backlog items. Other workflow documents
keep their current word limits.

## Markdown and links

| ID | Check |
| --- | --- |
| MD001 | A selected `remark-lint` rule found a Markdown structure problem. |
| LINK001 | A local link or image points to a missing file. |
| LINK002 | A local link points to a missing heading anchor. |

The selected lint rules cover heading levels, heading-like text,
duplicate definitions, empty link URLs, undefined references, and
media syntax. Markdown permits many unusual forms. A successful check
does not prove that every intended link or heading was written.
External web links are outside this check.

The validator parses Markdown with `remark` and GitHub Flavored
Markdown support. It uses `unified-engine` to give
`remark-validate-links` the files needed for cross-file anchor checks.
The validator collects library findings and prints them in stable order.
The package lock fixes the library versions for CI.

## Feature Briefs and backlog

| ID | Check |
| --- | --- |
| FB001 | A brief has exactly one nonempty H1. |
| FB002 | `Status` occurs once and is `Draft` or `Ready`. |
| FB003 | `Feature ID` occurs once, has form `B-xxxx`, and matches its directory. |
| FB004 | A named section occurs twice, or a required section is missing. |
| FB005 | A required section is empty or the stories section has no stories. |
| FB006 | A story ID occurs twice. |
| FB007 | Story IDs do not run from `S1` in document order. |
| FB008 | A story has no `Story:` statement or has more than one. |
| FB009 | A story has no `Acceptance:` block or has more than one. |
| FB010 | An acceptance block has no list criterion. |
| FB011 | Story content or subheadings have an invalid position or form. |
| FB012 | A brief has no matching backlog item. |
| FB013 | A backlog item has no canonical brief link or has a wrong link. |
| FB014 | A backlog ID occurs twice. |
| FB016 | A Feature ID occurs in more than one brief. |
| FB017 | A brief is outside `.workflow/features/B-xxxx/brief.md`. |
| SIZE001 | A document exceeds its whole-document hard word limit. |
| SIZE002 | A backlog item or Context entry exceeds its hard word limit. |

`Goal`, `Stories and acceptance`, `Scope`, and `Non-goals` are
required sections. `Feature-wide constraints and acceptance`,
`Related records`, and `Open questions and assumptions` are optional.
Every named section may occur at most once. Story headings are H3
headings inside `Stories and acceptance`.

For Draft, FB004 and FB005 findings for missing or empty required
content are warnings. FB007 through FB010 are warnings when content
is missing or story numbers have gaps. Duplicate statements and
blocks are errors for every status. Ready makes all completeness
findings errors. Identity, location, duplicate, link, and size findings
are always errors.

A backlog item normally uses `Feature Brief:` to link its canonical
brief. An older `Source:` link counts when it points to the same
canonical file. A `Source:` link to other material remains a source
link. Briefs without a matching backlog item fail.

The checker counts whitespace-separated source words. It preserves
the existing limits: Direction 4,000; each Direction topic 2,000;
Backlog 1,800; each backlog item 80; Context 1,500; each Context entry
80; each Feature Brief 1,000; each Acceptance Report 800; each PDR
500; and each ADR 700.

The checker does not judge vertical slices, scope boundaries,
acceptance sufficiency, material open questions, or whether Design
needs a product decision. Reviewers decide those matters.
