from __future__ import annotations

from typing import TextIO

from aoc.day_9_rope_bridge.geometry import Direction, Step


def parse_steps(stream: TextIO) -> list[Step]:
    out = []
    for line in map(str.strip, stream.readlines()):
        direction_, size = line.split(maxsplit=1)
        step = Step(getattr(Direction, direction_), int(size))
        out.append(step)

    return out
