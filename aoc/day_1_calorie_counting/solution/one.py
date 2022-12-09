from __future__ import annotations

from typing import TextIO

TEST_OUTPUT = 24_000


def solve(stream: TextIO) -> int:
    def flush() -> None:
        nonlocal num_calories, max_num_calories
        max_num_calories = max(num_calories, max_num_calories)
        num_calories = 0

    num_calories = max_num_calories = 0

    for line in map(str.strip, stream.readlines()):
        if len(line) == 0:
            flush()
        else:
            num_calories += int(line)

    flush()

    return max_num_calories
