from __future__ import annotations

from typing import TextIO

from aoc.day_10_cathode_ray_tube.cpu import CPU
from aoc.day_10_cathode_ray_tube.parser import parse_command
from aoc.day_10_cathode_ray_tube.utils import applymap


def solve(stream: TextIO) -> int:
    def callback(cpu: CPU) -> None:
        nonlocal out

        if (cpu.clock - 20) % 40 == 0:
            out += cpu.val * cpu.clock

    cpu = CPU()
    out = 0
    for line in map(str.strip, stream.readlines()):
        op = parse_command(line)
        applymap(callback, op.run(cpu))

    return out


def get_test_etalon() -> int:
    return 13140


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
