from __future__ import annotations

import enum
import functools
from typing import Generic, NamedTuple, TypeAlias, TypeVar

from typing_extensions import NamedTuple, Self

_T = TypeVar("_T")
_TT = TypeVar("_TT")


class Direction(enum.IntEnum):
    R = enum.auto()
    L = enum.auto()
    U = enum.auto()
    D = enum.auto()


class Step(NamedTuple):
    direction: Direction
    size: int


class _GridGeometry(NamedTuple, Generic[_T]):
    y: _T
    x: _T


_GridGeometryLike: TypeAlias = _TT | tuple[_T, _T]


class Shape(_GridGeometry[int]):
    pass


ShapeLike: TypeAlias = _GridGeometryLike[Shape, int]


class Border(_GridGeometry[range]):
    @functools.cached_property
    def shape(self) -> Shape:
        out = Shape(len(self.y), len(self.x))
        return out

    @classmethod
    def from_shape(cls, shape: ShapeLike) -> Self:
        out = cls(range(shape[1]), range(shape[0]))
        return out


class ClipLimit(_GridGeometry[tuple[int, int]]):
    pass


ClipLimitLike = _GridGeometryLike[ClipLimit, tuple[int, int]]


class Point(_GridGeometry[int]):
    @classmethod
    def default(cls) -> Self:
        out = cls(0, 0)
        return out

    def __add__(self, other: Self) -> Self:
        x = self.x + other.x
        y = self.y + other.y
        out = Point(y, x)

        return out

    def __sub__(self, other: Self) -> Self:
        x = self.x - other.x
        y = self.y - other.y
        out = Point(y, x)

        return out

    def abs(self) -> Self:
        x = abs(self.x)
        y = abs(self.y)
        out = Point(y, x)

        return out

    def step(self, direction: Direction) -> Self:
        y, x = self
        match direction:
            case Direction.R:
                x += 1
            case Direction.L:
                x -= 1
            case Direction.U:
                y += 1
            case Direction.D:
                y -= 1

        out = Point(y, x)

        return out

    def clip(self, *limits: tuple[int, int]) -> Self:
        out = Point(
            self._clip(self.y, limits[0]),
            self._clip(self.x, limits[1]),
        )
        return out

    @staticmethod
    def _clip(coord: int, limit: tuple[int, int]) -> int:
        if coord < limit[0]:
            coord = limit[0]

        if coord > limit[1]:
            coord = limit[1]

        return coord
