from __future__ import annotations

import itertools
import multiprocessing as mp
from typing import TextIO, cast

from aoc.day_15_beacon_exclusion_zone.geometry import Interval
from aoc.day_15_beacon_exclusion_zone.parser import parse_sensors
from aoc.day_15_beacon_exclusion_zone.sensor import Sensor, merge_coverages

X_MULTIPLIER = 4_000_000


def solve(stream: TextIO, cmax: int, num_workers: int | None = None, **_) -> int:
    sensors = parse_sensors(stream)
    search_interval = Interval(0, cmax + 1)

    if num_workers is None or num_workers in (0, 1):
        out = _solve_impl(sensors, search_interval, search_interval)

    else:
        with mp.Pool(num_workers) as pool:
            subanswers: list[int | None] = pool.starmap(
                _solve_impl,
                zip(
                    itertools.repeat(sensors),
                    search_interval.split(num_workers),
                    itertools.repeat(search_interval),
                ),
            )

        out = cast(int, next(iter(filter(bool, subanswers))))

    assert out is not None

    return out


def _solve_impl(
    sensors: list[Sensor], search_interval: Interval, clamp_interval: Interval
) -> int | None:
    out: int | None = None
    print(search_interval)
    for y in search_interval.range:
        coverage = merge_coverages(
            (sensor.coverage(y, with_beacon=True) for sensor in sensors)
        )
        coverage = coverage.clamp(clamp_interval)

        if coverage.size == len(clamp_interval):
            continue

        if len(coverage) == 1:
            interval = coverage[0]
            x = interval.lhs if interval.lhs != search_interval.lhs else interval.rhs

        elif len(coverage) == 2:
            x = coverage[0].rhs

        else:
            raise ValueError()

        out = x * X_MULTIPLIER + y
        break

    return out


def get_test_etalon() -> int:
    return 56000011


def get_test_solution(stream: TextIO) -> int:
    return solve(stream, 20)


def get_task_solution(stream: TextIO, num_workers: int | None = None, **_) -> int:
    return solve(stream, 4_000_000, num_workers)
