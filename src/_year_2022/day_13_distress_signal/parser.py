from __future__ import annotations

import itertools
from typing import Iterable, TextIO

from aoc.day_13_distress_signal.packet import Packet
from aoc.day_13_distress_signal.utils import chunked


def parse(stream: TextIO) -> Iterable[Packet]:
    for spec in chunked(map(str.strip, stream.readlines()), 3):
        yield from map(Packet.from_string, itertools.islice(spec, 2))
