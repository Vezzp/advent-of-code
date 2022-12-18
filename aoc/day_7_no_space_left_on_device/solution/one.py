from __future__ import annotations

import itertools
from typing import TextIO

from aoc.day_7_no_space_left_on_device.fs import Dir, FSObject
from aoc.day_7_no_space_left_on_device.parser import parse_filesystem

MAX_DIR_SIZE = 100_000


def solve(src: TextIO | Dir) -> int:
    if isinstance(src, Dir):
        root = src
    else:
        root = parse_filesystem(src)
    root.protect()

    out = 0
    for dir_ in filter(
        FSObject.is_dir,
        itertools.chain(itertools.repeat(root, 1), root.riterdir()),
    ):
        if (dir_size := dir_.size) <= MAX_DIR_SIZE:
            out += dir_size

    return out


def get_test_etalon() -> int:
    return 95437


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
