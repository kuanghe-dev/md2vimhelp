# md2vimhelp — technical notes

Single-file script, stdlib only (`re`, `sys`, `textwrap`, `pathlib`). Entry point and all
logic live in `md2vimhelp.py`.

## Conversion rules implemented

- A line matching `^# (.*)$` is a first-level **header** → rendered as `{title}~` (the
  Vim help convention for a highlighted section tag). A line matching `^## (.*)$` is a
  second-level **header** → rendered as `- {title}`. Only exactly one or two `#`s
  followed by a space triggers these — `###`+ is left as regular paragraph text (per
  explicit scope decision, not an oversight). The two patterns don't overlap: `^# `
  requires a space right after the single `#`, which `## ` never has.
- Leading tabs (at the start of a line) are expanded to 4 literal spaces per tab before
  parsing — not column-aligned `str.expandtabs()`, just a straight per-tab substitution.
  Tabs elsewhere in a line are left untouched. This runs once over the whole input, so it
  also applies inside fenced code blocks.
- A line matching `^```` (with or without a trailing language tag) opens a **fenced code
  block**; a line that is exactly ` ``` ` closes it. Interior lines are indented by 4
  spaces (blank interior lines stay blank, not padded with spaces). The fence lines
  themselves are dropped.
- Everything else is a **paragraph**: each source line is wrapped independently with
  `textwrap.fill(width=90)` — lines are *not* joined into one flowing block first (see
  `example/input3.md` / `example/output3.txt`, where the `Key points:` line and each
  following bullet stay on their own wrapped run).
- A paragraph line starting with a bullet marker (`- ` or `1. `, `2. `, etc.) gets a
  hanging indent on its wrapped continuation lines, aligned to the width of the marker
  (2 spaces for `- `, 3 spaces for `N. `).
- `**bold**` markers are stripped from header and paragraph text before wrapping (e.g.
  `**Keyword List**` → `Keyword List`). This does not apply inside fenced code blocks —
  content there is passed through untouched. Single-asterisk emphasis (`*word*`) is left
  alone.
- Whichever block (header or paragraph) immediately precedes a code block gets `" >"`
  appended to the *last* line of its rendered output — the Vim help convention marking
  the start of a preformatted region. This only applies when the preceding block is a
  header or paragraph — a code block immediately followed by another code block does
  *not* get `" >"` appended (see `example/input2.md` / `example/output2_correct.txt`).
- Blocks are joined with exactly one blank line between them in the output, regardless
  of how many blank lines separated them in the source (blank-line runs collapse to one).
- The file always ends with a blank line followed by a 90-dash divider line. No trailing
  Vim modeline (`vim:ft=help:`) is emitted.

## Parser design: why not "split on blank lines"

Fenced code blocks can contain **internal blank lines** (see the `## Durations` section
in `go-time.md`, or `## Adding/subtracting time`). A naive "blocks are separated by blank
lines" parser would incorrectly split one code block into two. `parse_blocks()` instead
runs an explicit two-state machine (`NORMAL` / `IN_CODE`):

- In `NORMAL`, a blank line ends the pending paragraph; a ` ``` ` line switches to
  `IN_CODE`; a `# ` or `## ` line closes any pending paragraph and emits a header block
  directly.
- In `IN_CODE`, every line (including blank ones) is code content until a closing ` ``` `
  fence is seen.

This is the load-bearing design decision in the file — don't "simplify" it back to a
blank-line split without re-checking that fixture.

## Overwrite behavior

- Two args (`input output`): output is written unconditionally.
- One arg (`input` only): output path = input path with `.md` → `.txt`. If that path
  already exists, prompt `y/N` on stdin and abort (exit 1) on anything but `y`.
