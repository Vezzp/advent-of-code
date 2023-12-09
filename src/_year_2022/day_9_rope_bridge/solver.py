from __future__ import annotations

from typing import Callable, TextIO

from aoc.day_9_rope_bridge.geometry import Point
from aoc.day_9_rope_bridge.parser import parse_steps
from aoc.day_9_rope_bridge.rope import Rope


def make_solver(num_knots: int) -> Callable[[TextIO], int]:
    def solve(stream: TextIO) -> int:
        steps = parse_steps(stream)

        path: set[Point] = {Point.default()}
        knot = Rope.default(num_knots=num_knots)

        for direction, size in steps:
            for _ in range(size):
                knot = knot.step(direction)
                path.add(knot.tail)

        out = len(path)

        return out

    return solve
