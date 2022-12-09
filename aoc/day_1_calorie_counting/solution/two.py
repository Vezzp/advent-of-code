from __future__ import annotations

import heapq
from typing import TextIO

TEST_OUTPUT = 45_000


def solve(stream: TextIO) -> int:
    def flush() -> None:
        nonlocal num_calories, heap
        if len(heap) >= 3:
            heapq.heappushpop(heap, num_calories)
        else:
            heapq.heappush(heap, num_calories)

        num_calories = 0

    heap = []
    num_calories = 0

    for line in map(str.strip, stream.readlines()):
        if len(line) == 0:
            flush()
        else:
            num_calories += int(line)

    flush()
    out = sum(heap)

    return out
