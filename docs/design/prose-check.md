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
accumulates a failing exit status. It returns each checker's native findings.
The model also receives STE100 warnings and uses its judgment to fix valid
findings. Checker or setup failures cannot pass as clean checks.

`--vocabulary-report` collects `STE-VOCAB-UNAPPROVED` findings across its
Markdown inputs. It prints one count per word, with the largest count first.
It groups words without regard to case. It accepts file paths and quoted glob
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
evidence for a glossary entry. Prefer vocabulary maintenance when rewriting a
legitimate term would reduce precision, clarity, or consistency.

A consuming project first adds useful local words to its project glossary. If
repeated use suggests a term is useful across projects, propose its promotion
to shared vocabulary. Make and review the shared change in `ofweb/skills`
before it becomes part of the common language profile. Keep canonical project
concepts in `.workflow/context.md`. Do not edit the installed skill copy from
the consuming project.

The project glossary is optional. It contains `technical_nouns` and
`technical_verbs` lists. Each item is a word or an object with `word` and
optional `inflections`. It does not contain meanings or feature behavior.
For example:

```json
{
  "technical_nouns": ["redstone", "amethyst", "biome", "Nautilus"]
}
```

For each input, find the project root from an explicit `--project-root` option
or by walking up from the file or current directory. A Context file or project
glossary identifies the root. Merge shared vocabulary, the optional project
glossary, and optional Context entries into a temporary glossary. Reject
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

STE100 permits possessive forms such as `owner's`. The pinned
`asd-ste100-checker`
revision `e193ecdd66b09ce81b7c611f1c841efd8ba84cc7` incorrectly reports
possessive `'s` as unknown vocabulary because of tokenization. `prose-check`
filters a finding only when it points to the actual possessive suffix. This is
a compatibility workaround for that checker revision, not an STE100 rule.
Contractions such as `it's`, `there's`, `don't`, and `isn't` still fail normally.

GFM tables and YAML frontmatter receive no special treatment in this version.
Collect unknown words before a repair pass. Classify them by vocabulary source
or rewrite unnecessary words. Rerun STE100 after each pass. Once STE100 passes,
fix Vale findings and rerun the checker. Treat findings as work to complete.
Report them only when a semantic decision prevents a safe fix.

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
