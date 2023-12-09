import re
from pathlib import Path
from types import MappingProxyType

import jogtrot

SPELL_TO_DIGIT = MappingProxyType(
    {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
)

DIGITS_RE = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")


def solve(rows: list[str]) -> int:
    out = 0
    for row in rows:
        digits = DIGITS_RE.findall(row)
        lhs = SPELL_TO_DIGIT[digits[0]]
        rhs = SPELL_TO_DIGIT[digits[-1]]
        out += int(f"{lhs}{rhs}")
    return out


def solve_first_part(__p: Path, /) -> None:
    rows = jogtrot.read_file_rows(__p)
    solution = solve(rows)
    jogtrot.print_solution(1, solution)


def solve_second_part(__p: Path, /) -> None:
    rows = jogtrot.read_file_rows(__p)
    solution = solve(rows)
    jogtrot.print_solution(2, solution)


def main() -> None:
    parts, input = jogtrot.parse_command_line()
    for part in parts:
        match part:
            case 1:
                solve_first_part(input)
            case 2:
                solve_second_part(input)
            case _:
                raise RuntimeError(f"Part {part} is not supported")


if __name__ == "__main__":
    main()
