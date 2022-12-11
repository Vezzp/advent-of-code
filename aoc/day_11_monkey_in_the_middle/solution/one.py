from __future__ import annotations

import heapq
import operator
from typing import TextIO

from aoc.day_11_monkey_in_the_middle.parser import parse_monkeys

TEST_OUTPUT = 10605


def solve(stream: TextIO) -> int:
    monkeys = parse_monkeys(stream)
    counters = [0] * len(monkeys)

    relief = lambda worry_level: worry_level // 3

    for _ in range(20):
        for idx, monkey in enumerate(monkeys):
            counters[idx] += len(monkey.items)
            monkey.play(monkeys, relief)

    out = operator.mul(*heapq.nlargest(2, counters))

    return out
