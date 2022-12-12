from __future__ import annotations

import dataclasses
from collections import deque
from typing import Callable, Iterable, NamedTuple, TextIO, TypeAlias

from typing_extensions import Self

from aoc.day_12_hill_climbing_algorithm.geometry import Grid, Point

TransitionStrategy: TypeAlias = Callable[["Route", Point], Iterable[Point]]

SRC_CHAR = "S"
DST_CHAR = "E"


class Step(NamedTuple):
    point: Point
    score: int


@dataclasses.dataclass
class Route:
    src: Point
    dst: Point
    landscape: Grid

    def __invert__(self) -> Self:
        return Route(self.dst, self.src, self.landscape)

    @classmethod
    def from_description(cls, stream: TextIO) -> Self:
        desc = tuple(map(str.strip, stream.readlines()))
        src: Point | None = None
        dst: Point | None = None
        landscape = Grid.zeros((len(desc), len(desc[0])))

        for y, row in enumerate(desc):
            for x, char in enumerate(row):
                point = Point(y, x)

                if char == SRC_CHAR:
                    src = point
                if char == DST_CHAR:
                    dst = point

                landscape[point] = _resolve_elevation_from_char(char)

        assert src is not None
        assert dst is not None

        out = cls(src, dst, landscape)

        return out

    def find_distances(
        self, transition_strategy: Callable[[Grid, Point], Iterable[Point]]
    ) -> Grid:
        grid = Grid.fill(self.landscape.shape, -1)

        visited: set[Point] = set()
        steps = deque([Step(self.src, 0)])

        while steps:
            point, score = steps.popleft()
            if point in visited:
                continue

            visited.add(point)
            grid[point] = score

            for neighbour in transition_strategy(self.landscape, point):
                if neighbour in visited:
                    continue
                steps.append(Step(neighbour, score + 1))

        return grid


def _resolve_elevation_from_char(char: str) -> int:
    if char == SRC_CHAR:
        repr_ = "a"
    elif char == DST_CHAR:
        repr_ = "z"
    else:
        repr_ = char

    out = ord(repr_) - ord("a")

    return out
