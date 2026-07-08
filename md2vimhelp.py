#!/usr/bin/env python3
import re
import sys
import textwrap
from pathlib import Path

WRAP_WIDTH = 90
TAB_WIDTH = 4
DIVIDER = "-" * WRAP_WIDTH
HEADER1_RE = re.compile(r"^# (.*)$")
HEADER2_RE = re.compile(r"^## (.*)$")
FENCE_RE = re.compile(r"^```")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
BULLET_RE = re.compile(r"^(-\s+|\d+\.\s+)")
LEADING_TABS_RE = re.compile(r"^\t+", re.MULTILINE)


def strip_bold(line: str) -> str:
    return BOLD_RE.sub(r"\1", line)


def wrap_line(line: str) -> list[str]:
    bullet_match = BULLET_RE.match(line)
    indent = " " * len(bullet_match.group(1)) if bullet_match else ""
    return textwrap.fill(line, width=WRAP_WIDTH, subsequent_indent=indent).splitlines()


def parse_blocks(text: str) -> list[tuple[str, list[str]]]:
    text = LEADING_TABS_RE.sub(lambda m: " " * TAB_WIDTH * len(m.group()), text)
    blocks: list[tuple[str, list[str]]] = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(("para", paragraph.copy()))
            paragraph.clear()

    for line in text.splitlines():
        if in_code:
            if line.strip() == "```":
                blocks.append(("code", code.copy()))
                code.clear()
                in_code = False
            else:
                code.append(line)
            continue

        header2_match = HEADER2_RE.match(line)
        header1_match = HEADER1_RE.match(line)
        if header2_match:
            flush_paragraph()
            blocks.append(("header2", [strip_bold(header2_match.group(1))]))
        elif header1_match:
            flush_paragraph()
            blocks.append(("header1", [strip_bold(header1_match.group(1))]))
        elif FENCE_RE.match(line):
            flush_paragraph()
            in_code = True
        elif line.strip() == "":
            flush_paragraph()
        else:
            paragraph.append(strip_bold(line))

    flush_paragraph()
    return blocks


def render(blocks: list[tuple[str, list[str]]]) -> str:
    rendered: list[list[str]] = []
    for i, (kind, lines) in enumerate(blocks):
        if kind == "header2":
            out = [f"- {lines[0]}"]
        elif kind == "header1":
            out = [f"{lines[0]}~"]
        elif kind == "code":
            out = [f"    {line}" if line.strip() else "" for line in lines]
        else:
            out = [wrapped for line in lines for wrapped in wrap_line(line)]

        next_is_code = i + 1 < len(blocks) and blocks[i + 1][0] == "code"
        if next_is_code and kind != "code" and out:
            out[-1] += " >"

        rendered.append(out)

    output_lines: list[str] = []
    for out in rendered:
        if output_lines:
            output_lines.append("")
        output_lines.extend(out)

    output_lines.append("")
    output_lines.append(DIVIDER)
    return "\n".join(output_lines) + "\n"


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print(f"Usage: {sys.argv[0]} <input.md> [output.txt]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_suffix(".txt")
        if output_path.exists():
            answer = input(f"{output_path} already exists. Overwrite? [y/N] ")
            if answer.strip().lower() != "y":
                print("Aborted.", file=sys.stderr)
                sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    output_path.write_text(render(blocks), encoding="utf-8")
    print(f"Finished writing output file: {output_path.resolve()}")


if __name__ == "__main__":
    main()
