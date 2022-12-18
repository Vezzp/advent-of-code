from __future__ import annotations

from typing import TextIO

from aoc.day_15_beacon_exclusion_zone.parser import parse_sensors
from aoc.day_15_beacon_exclusion_zone.sensor import merge_coverages


def solve(stream: TextIO, y: int) -> int:
    sensors = parse_sensors(stream)
    coverage = merge_coverages((sensor.coverage(y) for sensor in sensors))
    out = coverage.size

    return out


def get_test_etalon() -> int:
    return 26


def get_test_solution(stream: TextIO) -> int:
    return solve(stream, 10)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream, 2_000_000)
