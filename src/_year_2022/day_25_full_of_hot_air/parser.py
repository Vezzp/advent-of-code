from __future__ import annotations

from typing import TextIO


def parse(stream: TextIO) -> list[str]:
    out = list(map(str.strip, stream.readlines()))
    return out
