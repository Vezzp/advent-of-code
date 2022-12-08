from __future__ import annotations

from typing import TextIO

from aoc.day_8_treetop_tree_house.forest import Forest, ForestVisibilityMap
from aoc.day_8_treetop_tree_house.parser import parse_forest_data

TEST_OUTPUT = 21


def solve(stream: TextIO) -> int:
    forest = Forest.from_stream(stream, parse_forest_data)
    forest_visibility_map = ForestVisibilityMap.from_forest(forest)
    out = forest_visibility_map.num_trees

    return out
