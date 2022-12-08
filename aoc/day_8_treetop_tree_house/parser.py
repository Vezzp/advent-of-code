from __future__ import annotations

from typing import TextIO


def parse_forest_data(stream: TextIO) -> list[list[int]]:
    out = []
    for line in map(str.strip, stream.readlines()):
        row = list(map(int, line))
        out.append(row)

    return out
