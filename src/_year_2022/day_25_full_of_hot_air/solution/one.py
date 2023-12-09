from __future__ import annotations

from typing import TextIO

from aoc.day_25_full_of_hot_air.converter import (
    convert_decimal_to_snafu,
    convert_snafu_to_decimal,
)
from aoc.day_25_full_of_hot_air.parser import parse


def solve(stream: TextIO) -> str:
    snafu_numbers = parse(stream)
    decimal = sum(map(convert_snafu_to_decimal, snafu_numbers))
    out = convert_decimal_to_snafu(decimal)

    return out


def get_test_etalon() -> str:
    return "2=-1=0"


def get_test_solution(stream: TextIO, **_) -> ...:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> ...:
    return solve(stream)
