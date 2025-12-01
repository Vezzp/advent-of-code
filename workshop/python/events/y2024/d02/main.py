from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import assert_never
import itertools

import elf


def check_if_safe_report(values: Sequence[int], /) -> bool:
    assert len(values) > 1
    expected_cmp_result = elf.cmp(values[0], values[1])
    if expected_cmp_result == 0:
        return False
    return all(
        elf.cmp(lhs, rhs) == expected_cmp_result and (1 <= abs(lhs - rhs) <= 3)
        for lhs, rhs in itertools.pairwise(values)
    )


def solve_first_part(__p: Path, /) -> None:
    rows = elf.read_file_rows(__p)
    n_safe_reports = sum(
        check_if_safe_report([int(x) for x in row.strip().split()]) for row in rows
    )
    elf.print_solution(1, n_safe_reports)


def solve_second_part(__p: Path, /) -> None:
    rows = elf.read_file_rows(__p)
    n_safe_reports = 0
    for row in rows:
        values = [int(x) for x in row.strip().split()]
        n_safe_reports += int(
            check_if_safe_report(values)
            or any(
                check_if_safe_report(
                    [v for idx, v in enumerate(values) if idx != skip_idx]
                )
                for skip_idx in range(len(values))
            )
        )

    elf.print_solution(2, n_safe_reports)


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
