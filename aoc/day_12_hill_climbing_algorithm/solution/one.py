from __future__ import annotations

from typing import Iterable, TextIO

from aoc.day_12_hill_climbing_algorithm.geometry import Grid, Point
from aoc.day_12_hill_climbing_algorithm.route import Route


def transition_strategy(landscape: Grid, point: Point) -> Iterable[Point]:
    height = landscape[point] + 1
    for neighbour in landscape.border.neighbours(point):
        if height >= landscape[neighbour]:
            yield neighbour


def solve(stream: TextIO) -> int:
    route = Route.from_description(stream)
    distances = route.find_distances(transition_strategy)
    out = distances[route.dst]

    return out


def get_test_etalon() -> int:
    return 31


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
