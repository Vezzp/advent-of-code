from __future__ import annotations

from typing import TextIO

from aoc.day_13_distress_signal.packet import Packet
from aoc.day_13_distress_signal.parser import parse

TEST_OUTPUT = 140

DIVIDER_PACKAGES = (Packet([2]), Packet([6]))


def solve(stream: TextIO) -> int:
    packages = [*DIVIDER_PACKAGES, *parse(stream)]
    packages.sort()

    out = 1
    for package in DIVIDER_PACKAGES:
        out *= packages.index(package) + 1

    return out
