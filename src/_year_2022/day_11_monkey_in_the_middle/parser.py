from __future__ import annotations

import itertools
from typing import Iterable, TextIO, TypeVar

from aoc.day_11_monkey_in_the_middle.monkey import Monkey

MONKEY_SPEC_SIZE = 7


_T = TypeVar("_T")


def parse_monkeys(stream: TextIO) -> list[Monkey]:
    out = []
    for monkey_spec in ichunked(stream.readlines(), MONKEY_SPEC_SIZE):
        monkey = Monkey.from_description(monkey_spec)
        out.append(monkey)

    return out


def ichunked(lst: list[_T], chunk_size: int) -> Iterable[Iterable[_T]]:
    start_idx = 0
    for _ in range(len(lst) // chunk_size + 1):
        yield itertools.islice(lst, start_idx, (start_idx := start_idx + chunk_size))
