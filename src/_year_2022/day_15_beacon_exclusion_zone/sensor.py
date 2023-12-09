from __future__ import annotations

import dataclasses
import itertools
import operator
import re
from typing import Iterable, cast

from typing_extensions import Self, TypedDict

from aoc.day_15_beacon_exclusion_zone.geometry import Interval, Point

SENSOR_RE = re.compile(
    r"Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): "
    r"closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)"
)


class ParsedDescription(TypedDict):
    sx: str
    sy: str
    bx: str
    by: str


class Coverage(list[Interval]):
    @property
    def size(self) -> int:
        out = sum(len(interval) for interval in self)
        return out

    def clamp(self, interval: Interval) -> Self:
        out = Coverage()
        for interval_ in self:
            out.append(interval_.clamp(interval))
        return out


def merge_coverages(coverages: Iterable[Coverage]) -> Coverage:
    intervals = sorted(
        itertools.chain.from_iterable(coverages),
        key=operator.itemgetter(0),
        reverse=True,
    )
    out = Coverage()
    while len(intervals) > 1:
        lhs = intervals.pop()
        rhs = intervals[-1]

        if lhs[1] < rhs[0]:
            out.append(lhs)

        else:
            intervals.pop()
            intervals.append(Interval(lhs[0], max(lhs[1], rhs[1])))

    out.extend(intervals)

    return out


@dataclasses.dataclass(frozen=True, slots=True)
class Sensor:
    pos: Point
    beacon: Point

    @classmethod
    def from_description(cls, s: str, /) -> Self:
        parsed_description = cast(ParsedDescription, SENSOR_RE.match(s))
        pos = Point(
            int(parsed_description["sy"]),
            int(parsed_description["sx"]),
        )
        beacon = Point(
            int(parsed_description["by"]),
            int(parsed_description["bx"]),
        )
        out = cls(pos, beacon)

        return out

    @property
    def visibility(self) -> int:
        out = self.pos.distance(self.beacon)
        return out

    def coverage(self, y: int, with_beacon: bool = False) -> Coverage:
        coverage = Coverage()
        if (xdist := self.visibility - abs(self.pos.y - y)) < 0:
            return coverage

        xmin = self.pos.x - xdist
        xmax = self.pos.x + xdist

        if self.beacon.y != y or with_beacon:
            xmax += 1

        elif self.beacon.x == xmin:
            xmin += 1
            xmax += 1

        if xmax > xmin:
            coverage.append(Interval(xmin, xmax))

        return coverage
