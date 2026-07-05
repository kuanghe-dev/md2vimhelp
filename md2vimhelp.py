#!/usr/bin/env python3
import re
import sys
import textwrap
from pathlib import Path

WRAP_WIDTH = 90
DIVIDER = "-" * WRAP_WIDTH
HEADER_RE = re.compile(r"^## (.*)$")
FENCE_RE = re.compile(r"^```")


def parse_blocks(text: str) -> list[tuple[str, list[str]]]:
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

        header_match = HEADER_RE.match(line)
        if header_match:
            flush_paragraph()
            blocks.append(("header", [header_match.group(1)]))
        elif FENCE_RE.match(line):
            flush_paragraph()
            in_code = True
        elif line.strip() == "":
            flush_paragraph()
        else:
            paragraph.append(line)

    flush_paragraph()
    return blocks


def render(blocks: list[tuple[str, list[str]]]) -> str:
    rendered: list[list[str]] = []
    for i, (kind, lines) in enumerate(blocks):
        if kind == "header":
            out = [f"- {lines[0]}"]
        elif kind == "code":
            out = [f"    {line}" if line.strip() else "" for line in lines]
        else:
            out = textwrap.fill(" ".join(lines), width=WRAP_WIDTH).splitlines()

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


if __name__ == "__main__":
    main()
