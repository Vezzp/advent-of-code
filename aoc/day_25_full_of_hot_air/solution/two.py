from __future__ import annotations

from typing import TextIO


def solve(stream: TextIO) -> ...:
    ...


def get_test_etalon() -> ...:
    return ...


def get_test_solution(stream: TextIO, **_) -> ...:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> ...:
    return solve(stream)
