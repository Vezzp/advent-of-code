import argparse
from pathlib import Path
from typing import Any, Literal


def read_file_rows(path: Path, /) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)

    out = path.read_text().splitlines()
    if len(out) == 0:
        raise RuntimeError(f"File {path} is empty")

    return out


def print_solution(part: Literal[1, 2], solution: Any) -> None:
    print(f"Part {part} solution: {solution}")


def parse_command_line() -> tuple[list[Literal[1, 2]], Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="Puzzle part to solve", required=True)
    parser.add_argument("-i", help="File with puzzle input", required=True)

    args = parser.parse_args()
    parts: list[Literal[1, 2]]
    match args.p:
        case "1":
            parts = [1]
        case "2":
            parts = [2]
        case _:
            parts = [1, 2]

    return parts, Path(args.i)
