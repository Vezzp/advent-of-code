from __future__ import annotations

from typing import TextIO

from aoc.day_15_beacon_exclusion_zone.sensor import Sensor


def parse_sensors(stream: TextIO) -> list[Sensor]:
    out = [Sensor.from_description(line) for line in map(str.strip, stream.readlines())]
    return out
