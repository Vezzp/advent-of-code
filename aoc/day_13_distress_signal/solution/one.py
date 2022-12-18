from __future__ import annotations

from typing import TextIO

from aoc.day_13_distress_signal.parser import parse
from aoc.day_13_distress_signal.utils import chunked


def solve(stream: TextIO) -> int:
    out = 0
    for idx, (lhs, rhs) in enumerate(chunked(parse(stream), 2)):
        out += (idx + 1) * int(lhs <= rhs)

    return out


def get_test_etalon() -> int:
    return 13


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
