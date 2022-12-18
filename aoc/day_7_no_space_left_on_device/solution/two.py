from __future__ import annotations

from typing import TextIO

from aoc.day_7_no_space_left_on_device.fs import Dir, FSObject
from aoc.day_7_no_space_left_on_device.parser import parse_filesystem

MAX_FILESYSTEM_SIZE = 70_000_000
MIN_AVAILABLE_SIZE = 30_000_000


def solve(src: TextIO | Dir) -> int:
    if isinstance(src, Dir):
        root = src
    else:
        root = parse_filesystem(src)
    root.protect()

    drop_dir = root
    free_space = MAX_FILESYSTEM_SIZE - drop_dir.size

    for dir_ in filter(FSObject.is_dir, root.riterdir()):
        if free_space + dir_.size >= MIN_AVAILABLE_SIZE and drop_dir.size > dir_.size:
            drop_dir = dir_

    out = drop_dir.size

    return out


def get_test_etalon() -> int:
    return 24933642


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
