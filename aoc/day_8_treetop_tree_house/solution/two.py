from __future__ import annotations

from typing import TextIO

from aoc.day_8_treetop_tree_house.forest import Forest, ForestScenicMap
from aoc.day_8_treetop_tree_house.parser import parse_forest_data

TEST_OUTPUT = 8


def solve(stream: TextIO) -> int:
    forest = Forest.from_stream(stream, parse_forest_data)
    forest_scenic_map = ForestScenicMap.from_forest(forest)
    out = forest_scenic_map.max_score.score

    return out
