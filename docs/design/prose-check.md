# Markdown prose check

Status: Implemented.

`prose-check` accepts Markdown from standard input or file paths. When a model
changes prose in a Markdown file, it checks the complete file. For source
documentation comments and commit messages, pass the authored prose on standard
input. The command treats standard input as Markdown-compatible plain text.
Vale handles Markdown markup and excludes code blocks and inline code. Full
source-file comment extraction is outside this command.

Vale reads standard input when its command has no file argument. The wrapper
uses `--ext=.md` and `--path=stdin.md` to select Markdown checking. It does not
pass `-` as a file argument because Vale would skip stdin prose.

Install Vale separately. Install the repository script as a symlink on `PATH`
so it remains available as `prose-check` and uses the Vale configuration beside
the source. The wrapper needs only Python's standard library and Vale.

For each input, the command runs Vale with the bundled `.vale.ini` and styles.
It prints the source label and Vale's findings, continues to the next input
after a failure, and accumulates a failing exit status. Exit status 0 means
no blocking findings, 1 means lint failure, and 2 means a tool or input failure.
Checker or setup failures cannot pass as clean checks.

The configuration retains the Vale and Slop styles, including checks for
ceremony, hedging, vague reasons, unnecessary transitions, self-praise,
restating code, and other LLM-style prose. Spelling and term enforcement remain
disabled. The command does not validate vocabulary, read project glossaries or
Context, or enforce sentence word limits.

Document-specific skills decide what belongs in each document. Apply
`concise-prose` while writing, then fix useful Vale findings and rerun until
clean or until a finding would require changing intended meaning. Preserve
that meaning and explain any remaining finding.

Verify standard input, Markdown files, code exclusion, multiple inputs, lint
findings, tool failures, and missing inputs. Check that findings point to the
original file location and that later inputs run after an earlier failure.
