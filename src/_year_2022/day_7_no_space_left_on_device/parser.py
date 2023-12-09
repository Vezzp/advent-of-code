from __future__ import annotations

from typing import TextIO

from aoc.day_7_no_space_left_on_device.fs import Dir


def parse_filesystem(stream: TextIO) -> Dir:
    fs = Dir.empty_filesystem()
    curr_dir = fs

    for line in map(str.strip, stream.readlines()):
        match line.split():
            case ["__debug_stop__", *_]:
                break

            case ["$", "cd", dirname]:
                curr_dir = curr_dir.cd(dirname)

            case ["$", "ls"]:
                continue

            case ["dir", dirname]:
                curr_dir.mkdir(dirname)

            case [ssize, filename]:
                curr_dir.touch(filename, int(ssize))

            case _:
                raise RuntimeError(f"Line {line} does not satisfy task conditions")

    return fs
