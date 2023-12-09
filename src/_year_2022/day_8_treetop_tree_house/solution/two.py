from __future__ import annotations

from typing import TextIO

from aoc.day_8_treetop_tree_house.forest import Forest, ForestScenicMap
from aoc.day_8_treetop_tree_house.parser import parse_forest_data


def solve(stream: TextIO) -> int:
    forest = Forest.from_stream(stream, parse_forest_data)
    forest_scenic_map = ForestScenicMap.from_forest(forest)
    out = forest_scenic_map.max_score.score

    return out


def get_test_etalon() -> int:
    return 8


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
