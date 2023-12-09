from __future__ import annotations

import dataclasses
import itertools
import operator

from typing_extensions import Self

from aoc.day_9_rope_bridge.geometry import (
    Border,
    ClipLimit,
    Direction,
    Point,
    ShapeLike,
)

INT32_MAX = 2**31
INT32_MIN = -INT32_MAX


@dataclasses.dataclass
class Knot:
    head: Point
    tail: Point

    def step(self, direction: Direction | None) -> Self:
        head = self.head
        tail = self.tail

        if direction is not None:
            head = head.step(direction)

        match vec := tail - head:
            case [(-1 | 0 | 1), (-1 | 0 | 1)]:
                ...
            case _:
                tail -= (
                    vec.clip((-1, 1), (-1, 1))
                    if direction is None
                    else vec.step(direction)
                )

        self.head = head
        self.tail = tail

        return self

    @classmethod
    def default(cls) -> Self:
        out = cls(Point.default(), Point.default())
        return out


@dataclasses.dataclass
class Rope:
    knots: list[Knot]

    @property
    def num_knots(self) -> int:
        return len(self.knots)

    @classmethod
    def default(cls, num_knots: int) -> Self:
        out = cls([Knot.default() for _ in range(num_knots)])
        return out

    def step(self, direction: Direction) -> Self:
        prev_knot = curr_knot = self.knots[0].step(direction)

        for curr_knot in itertools.islice(self.knots, 1, self.num_knots):
            curr_knot.head = prev_knot.tail
            curr_knot.step(None)
            prev_knot = curr_knot

        return self

    @property
    def tail(self) -> Point:
        return self.knots[-1].head

    @property
    def head(self) -> Point:
        return self.knots[0].head

    def draw(self, shape: ShapeLike) -> str:
        border = Border.from_shape(shape)

        fill = "."
        grid = [[fill for _ in border.x] for _ in border.y]

        ymin = xmin = INT32_MAX
        for point in map(operator.attrgetter("head"), self.knots):
            ymin = min(point.y, ymin)
            xmin = min(point.x, xmin)

        offset = Point(ymin, xmin)
        for idx, point in enumerate(map(operator.attrgetter("head"), self.knots)):
            point_ = point - offset
            if grid[border.y[-1] - point_.y][point_.x] != fill:
                continue

            grid[border.y[-1] - point_.y][point_.x] = "H" if idx == 0 else f"{idx}"

        out = "\n".join(("".join(row) for row in grid))

        return out
