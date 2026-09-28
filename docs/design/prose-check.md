# Markdown prose check

Status: Implemented.

`prose-check` accepts Markdown from standard input or file paths. When a model
changes prose in a Markdown file, it checks the complete file. For source
documentation comments and commit messages, pass the authored prose on standard
input. The command treats standard input as Markdown-compatible plain text.
CommonMark markup, code blocks, and inline code are not STE input. Full
source-file comment extraction is outside this change.

Vale reads standard input when its command has no file argument. Do not pass
`-` as a file argument; that makes this Vale version silently skip stdin prose.

Install the repository script as a symlink on `PATH` so it remains available as
`prose-check` and uses the vocabulary and Vale configuration beside the source.

For each input, the command runs STE100 and then runs Vale only if that input
passes STE100. It continues to the next input after a checker finding and
accumulates a failing exit status. It returns STE100 findings after the narrow
compatibility and phrase filters, then returns Vale's findings.
The model also receives STE100 warnings and uses its judgment to fix valid
findings. Checker or setup failures cannot pass as clean checks.

`--vocabulary-report` collects `STE-VOCAB-UNAPPROVED` findings across its
Markdown inputs. It groups observed noun and verb forms under a candidate when
the base form is also observed. It prints the forms and their total count, with
the largest count first. It groups words without regard to case. It accepts file paths and quoted glob
patterns, including `**`. It excludes Markdown code through the normal prose
selection step. The report does not run Vale or edit files. Unknown words are
expected report data, so they do not cause a failing exit status. A missing
file, invalid project vocabulary, or checker failure does cause failure.

The existing Vale configuration remains the style source. STE100 uses its own
rules, built-in vocabulary, and the small shared software vocabulary beside
`prose-check`. `shared-terms.json` belongs to `ofweb/skills`. Add common
engineering and workflow terms there when they are broadly reusable. Treat an
installed copy as read-only in a consuming project. Project vocabulary has two
sources. Context defines concepts whose meaning must stay stable across project
work.
`.workflow/ste-glossary.json` approves intentional project or domain language
without a special canonical meaning. Repeated use across documents is strong
evidence that a term is intentional, but it does not approve the term alone.
Prefer a simpler STE100 rewrite when it preserves meaning. Approve vocabulary
only when replacement reduces precision, clarity, or consistency, or makes the
prose awkward. Be conservative with ordinary adjectives, abstract nouns,
jargon, and rare words.

A consuming project adds reviewed local words to its project glossary. If
repeated use suggests a term is useful across projects, propose its promotion
to shared vocabulary. Make and review the shared change in `ofweb/skills`
before it becomes part of the common language profile. Keep canonical project
concepts in `.workflow/context.md`. Do not edit the installed skill copy from
the consuming project.

The project glossary is optional. It contains an `approved_terms` list. Each
entry is a word or an object with `word` and optional `inflections` or
`part_of_speech`. Use only required forms. The glossary also accepts an
`exact_names` list for complete names that must remain verbatim. These names
are not approved vocabulary. Existing `technical_nouns` and `technical_verbs`
lists remain valid for compatibility. The project glossary does not contain
meanings or feature behavior.
For example:

```json
{
  "approved_terms": [
    {"word": "meal", "inflections": ["meals"]},
    {"word": "harvest", "part_of_speech": "verb", "inflections": ["harvests", "harvested"]}
  ],
  "exact_names": ["Farmer's Delight"]
}
```

The pinned checker accepts only technical noun and verb lists. It skips
part-of-speech mismatch checks for both kinds of technical term. The adapter
converts `approved_terms` to those lists without disabling other checker rules.
Run terms through `prose-check`; the source JSON is not a native checker glossary.
Optional grammatical metadata records intended usage, but this checker revision
does not enforce it for technical terms. Do not add a large adjective list or
use an approved term to redefine an ordinary STE100 word. Context keeps stable
concept meanings. A multi-word Context concept permits unknown words only
inside the complete phrase, such as `Job reservation`. Its parts do not gain
general approval.

For each input, find the project root from an explicit `--project-root` option
or by walking up from the file or current directory. A Context file or project
glossary identifies the root. Merge shared vocabulary, the optional project
glossary, and optional Context entries into a temporary checker glossary. Reject
malformed entries and duplicate terms or forms across these sources. Without
either project file, use shared terms alone. The merged glossary uses JSON, a
YAML-compatible format accepted by STE100. Derivation needs only the Python
standard library.

Use `cmark` to select Markdown text nodes. Replace non-prose characters with
spaces while preserving character offsets. Mark heading line endings as
sentence boundaries so headings cannot join the next prose block. Pass the
masked text to STE100. If it passes, run Vale on the original input. Print each
checker's findings with a source and checker label. Use a nonzero status for
blocking findings or tool failure.

Keep exact names and Context phrases in the text sent to STE100. Filter only
vocabulary findings that lie wholly inside a reviewed complete name or a
multi-word Context phrase. Filter part-of-speech findings inside exact names
when their tokens are name fragments. Leave sentence length, structure,
ambiguity, verb, and complexity findings intact.

STE100 permits possessive forms such as `owner's`. The pinned
`asd-ste100-checker`
revision `e193ecdd66b09ce81b7c611f1c841efd8ba84cc7` incorrectly reports
possessive `'s` as unknown vocabulary because of tokenization. `prose-check`
filters a finding only when it points to the actual possessive suffix. This is
a compatibility workaround for that checker revision, not an STE100 rule.
Contractions such as `it's`, `there's`, `don't`, and `isn't` still fail normally.

GFM tables and YAML frontmatter receive no special treatment in this version.

Collect all distinct unknown words before a repair pass. Check for a simpler
approved expression first. Search project documents when usage helps classify
a term as `rewrite`, `shared`, `project`, `context`, or `checker`. Rewrite safe
cases and investigate checker noise before review. Group observed word forms.
Present one compact review group with only necessary vocabulary candidates,
their source, forms, reason, and an example when useful. Do not present full
lint output unless requested. Apply accepted terms in their owning source and
rerun STE100. Rewrite remaining avoidable words. Once STE100 passes, fix Vale
findings and rerun the checker.

The tested STE100 revision is installed from GitHub because the named package
is not available from the package registry. Its spaCy model must be installed
in the uv tool environment:

    uv tool install 'git+https://github.com/sourdough-bread/asd-ste100-checker.git@e193ecdd66b09ce81b7c611f1c841efd8ba84cc7'
    VIRTUAL_ENV="$(uv tool dir)/asd-ste100-checker" ste100 setup

Install Vale and `cmark` separately.

Verify with a clean prose file, a file with a fenced and inline code sample,
standard input, multiple files, a checker error, and a missing checker. Check
that ignored code cannot produce STE findings, a finding still points to its
original file location, and Vale runs for passing inputs even when another
input fails STE100.
