import re
from pathlib import Path
from typing import assert_never, cast

import elf

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing_extensions import TypedDict

    class MatchedMul(TypedDict):
        lhs: str
        rhs: str


def solve_first_part(__p: Path, /) -> None:
    MUL_PATTERN = re.compile(r"mul\((?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})\)")
    rows = elf.read_file_rows(__p)
    solution = 0
    for matched_pat in MUL_PATTERN.finditer("".join(rows)):
        matched_mul = cast("MatchedMul", matched_pat.groupdict())
        solution += int(matched_mul["lhs"]) * int(matched_mul["rhs"])
    elf.print_solution(1, solution)


def solve_second_part(__p: Path, /) -> None:
    MUL_PATTERN = re.compile(
        r"do\(\)|don't\(\)|mul\((?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})\)"
    )
    rows = elf.read_file_rows(__p)
    solution = 0
    mul_enabled: bool = True
    for matched_pat in MUL_PATTERN.finditer("".join(rows)):
        match matched_pat.group(0):
            case "do()":
                mul_enabled = True
            case "don't()":
                mul_enabled = False
            case _ if mul_enabled:
                matched_mul = cast("MatchedMul", matched_pat.groupdict())
                solution += int(matched_mul["lhs"]) * int(matched_mul["rhs"])
    elf.print_solution(2, solution)


def main() -> None:
    parts, input = elf.parse_command_line()
    for part in parts:
        match part:
            case 1:
                solve_first_part(input)
            case 2:
                solve_second_part(input)
            case _:
                assert_never(part)


if __name__ == "__main__":
    main()
