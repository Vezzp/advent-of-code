from __future__ import annotations

from aoc.day_10_cathode_ray_tube.cpu import Addx, Noop, Op


def parse_command(line: str) -> Op:
    match line.split():
        case ["noop"]:
            out = Noop()
        case ["addx", addenum_]:
            out = Addx(int(addenum_))
        case _:
            raise ValueError(line)

    return out
