import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "md2vimhelp.py"
EXAMPLE_DIR = REPO_ROOT / "example"

CASES = ["example1", "example2", "example3"]


@pytest.mark.parametrize("name", CASES)
def test_conversion_matches_expected_output(name: str, tmp_path: Path) -> None:
    input_path = EXAMPLE_DIR / f"{name}.md"
    expected_path = EXAMPLE_DIR / f"{name}.txt"
    output_path = tmp_path / f"{name}.txt"

    subprocess.run(
        [sys.executable, str(SCRIPT), str(input_path), str(output_path)],
        check=True,
    )

    assert output_path.read_text(encoding="utf-8") == expected_path.read_text(encoding="utf-8")
