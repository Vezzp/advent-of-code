from __future__ import annotations

import functools
import itertools
import pprint
from typing import (
    Generator,
    Generic,
    Iterable,
    Literal,
    MutableSequence,
    NamedTuple,
    TypeAlias,
    TypeVar,
    Union,
)

from typing_extensions import NamedTuple, Self

_T = TypeVar("_T")
_TT = TypeVar("_TT")
_GridItemT = TypeVar("_GridItemT")


_GridGeometryLike: TypeAlias = _TT | tuple[_T, _T]
ShapeLike: TypeAlias = _GridGeometryLike["Shape", int]
PointLike: TypeAlias = _GridGeometryLike["Point", int]
IntervalLike: TypeAlias = _GridGeometryLike["Interval", int]
GridLike: TypeAlias = Union[MutableSequence[MutableSequence[int]], "Grid"]


class _GridGeometry(NamedTuple, Generic[_T]):
    y: _T
    x: _T


class Shape(_GridGeometry[int]):
    pass


class Interval(NamedTuple):
    lhs: int
    rhs: int

    def __len__(self) -> int:
        out = self.rhs - self.lhs
        return out

    @property
    def range(self) -> range:
        return range(self.lhs, self.rhs)

    def split(self, num_splits: int) -> Iterable[Self]:
        start = self.lhs
        chunk_size = len(self) // num_splits

        for _ in range(num_splits - 1):
            yield Interval(start, (start := start + chunk_size))

        yield Interval(start, self.rhs)

    def clamp(self, other: IntervalLike) -> Self:
        lhs = self._clamp(self.lhs, *other)
        rhs = self._clamp(self.rhs, *other)
        out = Interval(lhs, rhs)

        return out

    @staticmethod
    def _clamp(p: int, pmin: int, pmax: int) -> int:
        out = min(max(p, pmin), pmax)
        return out


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

    def __abs__(self) -> Self:
        out = Point(*map(abs, self))  # type: ignore
        return out

    def distance(self, other: Self, /, norm: Literal["l1"] = "l1") -> int:
        if norm == "l1":
            out = sum(abs(self - other))  # type: ignore
        else:
            raise NotImplementedError()

        return out


class Border(_GridGeometry[range]):
    @functools.cached_property
    def shape(self) -> Shape:
        out = Shape(len(self.y), len(self.x))
        return out

    @classmethod
    def from_shape(cls, shape: ShapeLike) -> Self:
        shape = Shape(*shape)
        out = cls(x=range(shape.x), y=range(shape.y))
        return out

    def __contains__(self, p: PointLike, /) -> bool:
        out = p[0] in self[0] and p[1] in self[1]
        return out

    def neighbours(self, p: PointLike) -> Iterable[Point]:
        p = Point(*p)
        for delta in (-1, 1):
            if (out := Point(p.y, p.x + delta)) in self:
                yield out
            if (out := Point(p.y + delta, p.x)) in self:
                yield out


class Grid(Generic[_GridItemT]):
    def __init__(self, data: list[list[_GridItemT]]) -> None:
        self._data = data

    def __getitem__(self, key: PointLike, /) -> _GridItemT:
        return self._data[key[0]][key[1]]

    def __setitem__(self, key: PointLike, val: _GridItemT, /) -> None:
        self._data[key[0]][key[1]] = val

    def __repr__(self) -> str:
        out = pprint.pformat(self._data)
        return out

    @functools.cached_property
    def border(self) -> Border:
        out = Border(x=range(len(self._data[0])), y=range(len(self._data)))
        return out

    @functools.cached_property
    def shape(self) -> Shape:
        out = self.border.shape
        return out

    @classmethod
    def fill(cls, shape: ShapeLike, fill: _GridItemT) -> Self:
        data = [[fill] * shape[1] for _ in range(shape[0])]
        out = cls(data)
        return out

    def ndenumerate(self) -> Generator[tuple[Point, _GridItemT], None, None]:
        for y, x in itertools.product(*self.border):
            yield (p := Point(y, x)), self[p]
