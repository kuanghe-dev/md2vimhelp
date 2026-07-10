# md2vimhelp

Convert a Markdown file into Vim's `:help` text format.

## Usage

Install it as a `md2vimhelp` command with [uv](https://docs.astral.sh/uv/):

```sh
uv tool install .
md2vimhelp input.md output.txt
```

Or run the script directly without installing:

```sh
python3 md2vimhelp.py input.md output.txt
```

Either way, you can omit the output path and it's derived by swapping the `.md`
extension for `.txt`:

```sh
md2vimhelp input.md   # writes input.txt
```

If the derived output file already exists, you'll be asked to confirm before it's
overwritten. Passing the output path explicitly always overwrites without asking.

## What it does

- `## Header` lines become `- Header` lines.
- Fenced code blocks (` ```go ` or ` ``` `) are indented by 4 spaces and the backtick
  fences are removed.
- Regular paragraphs are word-wrapped to a maximum of 90 characters per line.
- Whichever paragraph or header immediately precedes a code block gets `" >"` appended
  to its last line (the Vim help convention for introducing a preformatted block). A
  code block immediately followed by another code block does not get the marker.
- The file ends with a divider line of 90 dashes.

## Example

Input (`example/example1.md`):

```
## Getting the current time

​```go
now := time.Now()
​```
```

Output (`example/example1.txt`):

```
- Getting the current time >

    now := time.Now()
```

See `example/example1.md` and `example/example1.txt` for a full before/after.

## Development

Dependencies (currently just `pytest`) are managed with [uv](https://docs.astral.sh/uv/).

```sh
uv sync        # create .venv and install dev dependencies
uv run pytest  # run the test suite
```

`uv run` picks up the project's `.venv` automatically, so there's no need to activate it
by hand.
