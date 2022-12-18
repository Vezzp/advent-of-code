from __future__ import annotations

import textwrap
from typing import TextIO

from aoc.day_10_cathode_ray_tube.cpu import CPU
from aoc.day_10_cathode_ray_tube.crt import CRT
from aoc.day_10_cathode_ray_tube.parser import parse_command
from aoc.day_10_cathode_ray_tube.utils import applymap


def solve(stream: TextIO) -> str:
    cpu = CPU()
    crt = CRT()
    for line in map(str.strip, stream.readlines()):
        op = parse_command(line)
        applymap(crt.connect, op.run(cpu))

    out = str(crt)

    return out


def get_test_etalon() -> str:
    return textwrap.dedent(
        """\
        ##..##..##..##..##..##..##..##..##..##..
        ###...###...###...###...###...###...###.
        ####....####....####....####....####....
        #####.....#####.....#####.....#####.....
        ######......######......######......####
        #######.......#######.......#######....."""
    )


def get_test_solution(stream: TextIO, **_) -> str:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> str:
    return solve(stream)
