from __future__ import annotations

import dataclasses
import functools
import itertools
import operator
import pprint
from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    MutableSequence,
    TextIO,
    TypeAlias,
    TypeVar,
)

from typing_extensions import NamedTuple, Self

GridT = TypeVar("GridT", bound="Grid")
GridVisitor: TypeAlias = Callable[["GridT", tuple[int, int]], None]
GridRowT = TypeVar("GridRowT", bound=MutableSequence[int])

_T = TypeVar("_T")


class _GridGeometry(NamedTuple, Generic[_T]):
    y: _T
    x: _T


class Shape(_GridGeometry[int]):
    pass


class Point(_GridGeometry[int]):
    pass


class Border(_GridGeometry[range]):
    @functools.cached_property
    def shape(self) -> Shape:
        out = Shape(len(self.y), len(self.x))
        return out


@dataclasses.dataclass
class Tree:
    point: Point
    height: int


class ScenicScore(NamedTuple):
    point: Point
    score: int


class Grid(Generic[GridRowT]):
    def __init__(self, data: list[GridRowT]) -> None:
        self._data = data

    def __getitem__(self, __key: tuple[int, int] | Point, /) -> int:
        out = self._data[__key[0]][__key[1]]
        return out

    def __setitem__(self, __key: tuple[int, int] | Point, __val: int, /) -> None:
        self._data[__key[0]][__key[1]] = __val

    def __repr__(self) -> str:
        out = pprint.pformat(self._data)
        return out

    @classmethod
    def from_border(cls, border: Border) -> Self:
        out = cls([[0] * len(border.x) for _ in border.y])
        return out

    @functools.cached_property
    def border(self) -> Border:
        out = Border(x=range(len(self._data[0])), y=range(len(self._data)))
        return out

    @functools.cached_property
    def shape(self) -> Shape:
        out = self.border.shape
        return out

    def traverse(
        self,
        path: Iterable[tuple[int, int]],
        visitor: GridVisitor,
    ) -> None:
        for point in path:
            visitor(self, point)


class Forest(Grid[GridRowT]):
    @classmethod
    def from_stream(
        cls, stream: TextIO, parser: Callable[[TextIO], list[GridRowT]]
    ) -> Self:
        grid = parser(stream)
        out = cls(grid)

        return out

    def __getitem__(self, __key: tuple[int, int], /) -> Tree:
        point = Point(*__key)
        height = super().__getitem__(__key)
        out = Tree(point, height)

        return out

    def __iter__(self) -> Iterator[Tree]:
        for pos in zip(*self.border):
            yield self[pos]


class ForestVisibilityMap(Grid[list]):
    @classmethod
    def from_forest(cls, forest: Forest, /) -> Self:
        def make_visitor() -> GridVisitor:
            max_tree_height = -1

            def visitor(grid: Forest, point: tuple[int, int]) -> None:
                nonlocal max_tree_height
                if (tree_height := grid[point].height) > max_tree_height:
                    out[point] = 1
                    max_tree_height = tree_height

            return visitor

        out = cls.from_border(forest.border)

        for path in itertools.chain(
            # Left to right.
            (zip(forest.border.y, itertools.repeat(x)) for x in forest.border.x),
            # Right to left.
            (zip(forest.border.y[::-1], itertools.repeat(x)) for x in forest.border.x),
            # Up to bottom.
            (zip(itertools.repeat(y), forest.border.x) for y in forest.border.y),
            # Bottom to up.
            (zip(itertools.repeat(y), forest.border.x[::-1]) for y in forest.border.y),
        ):
            forest.traverse(path, make_visitor())

        return out

    @functools.cached_property
    def num_trees(self) -> int:
        out = sum(map(sum, self._data))
        return out


class ForestScenicMap(Grid[GridRowT]):
    @classmethod
    def from_forest(cls, forest: Forest) -> Self:
        def visitor(grid: Forest, point: tuple[int, int]) -> None:
            tree = grid[point]
            score_ = 1
            for points_ in (
                # Left trees.
                zip(
                    itertools.repeat(tree.point.y), grid.border.x[: tree.point.x][::-1]
                ),
                # Right trees.
                zip(itertools.repeat(tree.point.y), grid.border.x[tree.point.x + 1 :]),
                # Up trees.
                zip(
                    grid.border.y[: tree.point.y][::-1], itertools.repeat(tree.point.x)
                ),
                # Down trees.
                zip(grid.border.y[tree.point.y + 1 :], itertools.repeat(tree.point.x)),
            ):
                num_trees = 0
                for point_ in points_:
                    num_trees += 1
                    if grid[point_].height >= tree.height:
                        break

                score_ *= num_trees

            out[tree.point] = score_

        out = cls.from_border(forest.border)
        forest.traverse(
            itertools.product(forest.border.y[1:-1], forest.border.x[1:-1]), visitor
        )

        return out

    @functools.cached_property
    def max_score(self) -> ScenicScore:
        point_, score = max(
            (
                ((y, x), score)
                for y, row in enumerate(self._data)
                for x, score in enumerate(row)
            ),
            key=operator.itemgetter(1),
        )
        out = ScenicScore(Point(*point_), score)

        return out
