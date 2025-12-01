from pathlib import Path
from typing import assert_never

import elf


def solve_first_part(__p: Path, /) -> None:
    DIRECTIONS = (
        +1 + 0j,  # →
        -1 + 0j,  # ←
        +0 + 1j,  # ↓
        +0 - 1j,  # ↑
        +1 - 1j,  # ↘
        -1 - 1j,  # ↙
        +1 + 1j,  # ↗
        -1 + 1j,  # ↖
    )
    pos_to_char = {
        x + y * 1j: char
        for y, row in enumerate(elf.read_file_rows(__p))
        for x, char in enumerate(row)
    }
    solution = 0
    for direction in DIRECTIONS:
        for pos in pos_to_char:
            solution += int(
                all(
                    pos_to_char.get(pos + direction * step) == char
                    for step, char in enumerate("XMAS")
                )
            )
    elf.print_solution(1, solution)


def solve_second_part(__p: Path, /) -> None:
    DIRECTIONS = (
        -1 + 1j,  # ↖
        +1 + 1j,  # ↗
        +1 - 1j,  # ↘
        -1 - 1j,  # ↙
    )
    BORDERS = ("SSMM", "SMMS", "MMSS", "MSSM")
    pos_to_char = {
        x + y * 1j: char
        for y, row in enumerate(elf.read_file_rows(__p))
        for x, char in enumerate(row)
    }
    solution = 0
    for pos, char in pos_to_char.items():
        solution += int(
            char == "A"
            and (
                "".join(
                    pos_to_char.get(pos + direction, "") for direction in DIRECTIONS
                )
                in BORDERS
            )
        )
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
