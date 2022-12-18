from __future__ import annotations

from typing import TextIO

from aoc.day_9_rope_bridge.solver import make_solver

solve = make_solver(num_knots=2)


def get_test_etalon() -> int:
    return 13


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
