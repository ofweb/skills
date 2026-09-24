# Markdown prose check

Status: Implemented.

`prose-check` accepts Markdown from standard input or file paths. When a model
changes prose in a file, it checks the complete file. It runs Vale and the
ASD-STE100 checker on written text. CommonMark markup, code blocks, and inline
code are not STE input. Source comments are outside this change.

Install the repository script as a symlink on `PATH` so it remains available as
`prose-check` and uses the vocabulary and Vale configuration beside the source.

The command returns each checker's native findings. Vale and STE100 errors
block completion. The model also receives STE100 warnings and uses its judgment
to fix valid findings. It need not explain warnings it leaves. Checker or setup
failures cannot pass as clean checks.

The existing Vale configuration remains the style source. STE100 uses its own
rules, built-in vocabulary, and a small shared software vocabulary. The user
adds shared terms manually when a recurring technical concept needs a stable
name. The model may suggest a term but cannot add one itself. Context-derived
project terms are a separate change.

Use `cmark` to select Markdown text nodes. Replace non-prose characters with
spaces while preserving newlines and character offsets. Run Vale on the
original Markdown and pass the masked text to STE100. Print each checker's
native output with a source and checker label. Use a nonzero status for
blocking findings or tool failure.

GFM tables and YAML frontmatter receive no special treatment in this version.
Existing documents can fail on ordinary words outside the small shared
vocabulary; do not add those words automatically.

The tested STE100 revision is pinned in `SKILL.md`. It is installed from GitHub
because the named package is not available from the package registry. Its spaCy
model must be installed in the uv tool environment.

Verify with a clean prose file, a file with a fenced and inline code sample,
standard input, multiple files, a checker error, and a missing checker. Check
that ignored code cannot produce STE findings and that a finding still points
to its original file location.
