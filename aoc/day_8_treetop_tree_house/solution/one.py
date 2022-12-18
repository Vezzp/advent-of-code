from __future__ import annotations

from typing import TextIO

from aoc.day_8_treetop_tree_house.forest import Forest, ForestVisibilityMap
from aoc.day_8_treetop_tree_house.parser import parse_forest_data


def solve(stream: TextIO) -> int:
    forest = Forest.from_stream(stream, parse_forest_data)
    forest_visibility_map = ForestVisibilityMap.from_forest(forest)
    out = forest_visibility_map.num_trees

    return out


def get_test_etalon() -> int:
    return 21


def get_test_solution(stream: TextIO, **_) -> int:
    return solve(stream)


def get_task_solution(stream: TextIO, **_) -> int:
    return solve(stream)
