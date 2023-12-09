from __future__ import annotations

import heapq
import math
import operator
from typing import TextIO

from aoc.day_11_monkey_in_the_middle.parser import parse_monkeys


def solve(stream: TextIO) -> int:
    monkeys = parse_monkeys(stream)
    counters = [0] * len(monkeys)

    worry_lcm = math.lcm(*map(operator.attrgetter("test.divider"), monkeys))

    relief = lambda worry_level: worry_level % worry_lcm

    for _ in range(10_000):
        for idx, monkey in enumerate(monkeys):
            counters[idx] += len(monkey.items)
            monkey.play(monkeys, relief)

    out = operator.mul(*heapq.nlargest(2, counters))

    return out


def get_test_etalon() -> int:
    return 2713310158


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
