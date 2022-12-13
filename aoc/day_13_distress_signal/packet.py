from __future__ import annotations

import ast
import enum
import itertools
from typing import Iterable, TypeAlias, cast

from typing_extensions import Self

PacketDataType: TypeAlias = list[list[int] | int]


class Ordering(enum.IntEnum):
    LESS = enum.auto()
    EQUAL = enum.auto()
    GREATER = enum.auto()


class Packet(PacketDataType):
    @classmethod
    def from_string(cls, s: str, /) -> Self:
        out = cls(ast.literal_eval(s))
        return out

    def __le__(self, other: Self) -> bool:
        ordering = _cmp(self, other)
        match ordering:
            case Ordering.LESS | Ordering.EQUAL:
                return True
            case _:
                return False

    def __lt__(self, other: Self) -> bool:
        ordering = _cmp(self, other)
        match ordering:
            case Ordering.LESS:
                return True
            case _:
                return False

    def __eq__(self, other: Self) -> bool:
        return _cmp(self, other) is Ordering.EQUAL


def _cmp(lhs: PacketDataType, rhs: PacketDataType) -> Ordering:
    for lhs_, rhs_ in cast(
        Iterable[tuple[PacketDataType | None, PacketDataType | None]],
        itertools.zip_longest(lhs, rhs),
    ):
        match lhs_, rhs_:
            case [None, _]:
                return Ordering.LESS

            case [_, None]:
                return Ordering.GREATER

            case [int(), int()]:
                if lhs_ < rhs_:  # type: ignore
                    return Ordering.LESS
                if lhs_ > rhs_:  # type: ignore
                    return Ordering.GREATER

            case [int(), list()] | [list(), int()] | [list(), list()]:
                if isinstance(lhs_, int):
                    lhs_ = [lhs_]
                if isinstance(rhs_, int):
                    rhs_ = [rhs_]

                if (ordering := _cmp(lhs_, rhs_)) is not Ordering.EQUAL:
                    return ordering

            case _:
                raise ValueError(type(lhs_), type(rhs_))

    return Ordering.EQUAL
