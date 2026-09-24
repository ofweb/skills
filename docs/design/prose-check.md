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

The existing Vale configuration remains the style source. STE100 uses its own
rules, built-in vocabulary, and a small shared software vocabulary. The user
adds shared terms manually when a recurring technical concept needs a stable
name. The model may suggest a term but cannot add one itself. Context-derived
project terms are a separate change.

Use `cmark` to select Markdown text nodes. Replace non-prose characters with
spaces while preserving newlines and character offsets. Pass the masked text
to STE100. If it passes, run Vale on the original input. Print each checker's
native output with a source and checker label. Use a nonzero status for
blocking findings or tool failure.

GFM tables and YAML frontmatter receive no special treatment in this version.
Existing documents can fail on ordinary words outside the small shared
vocabulary; do not add those words automatically.

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
