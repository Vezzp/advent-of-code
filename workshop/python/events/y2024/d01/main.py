from collections import Counter
import operator
from pathlib import Path
from typing import assert_never

import elf


def parse_items(__p: Path, /) -> tuple[list[int], list[int]]:
    lhs_items: list[int] = []
    rhs_items: list[int] = []

    for lhs_item, rhs_item in (
        map(int, line.strip().split()) for line in __p.read_text().splitlines()
    ):
        lhs_items.append(lhs_item)
        rhs_items.append(rhs_item)

    return lhs_items, rhs_items


def solve_first_part(__p: Path, /) -> None:
    lhs_items, rhs_items = parse_items(__p)
    lhs_items.sort()
    rhs_items.sort()
    solution = sum(
        abs(operator.sub(*pair)) for pair in zip(lhs_items, rhs_items, strict=True)
    )
    elf.print_solution(1, solution)


def solve_second_part(__p: Path, /) -> None:
    lhs_items, rhs_items = parse_items(__p)
    rhs_items_counter = Counter(rhs_items)
    solution = sum(
        lhs_item * rhs_items_counter.get(lhs_item, 0) for lhs_item in lhs_items
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
