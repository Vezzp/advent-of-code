#!/usr/bin/env python3

import elf
from typing import List, Tuple


def parse_forest(lines: List[str]) -> List[List[int]]:
    grid = []
    for line in lines:
        line = line.strip()
        if line:
            grid.append([int(c) for c in line])
    return grid


def is_visible(grid: List[List[int]], row: int, col: int) -> bool:
    height = grid[row][col]
    rows = len(grid)
    cols = len(grid[0])

    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
        return True

    visible_from_left = all(grid[row][c] < height for c in range(col))
    visible_from_right = all(grid[row][c] < height for c in range(col + 1, cols))
    visible_from_top = all(grid[r][col] < height for r in range(row))
    visible_from_bottom = all(grid[r][col] < height for r in range(row + 1, rows))

    return (
        visible_from_left
        or visible_from_right
        or visible_from_top
        or visible_from_bottom
    )


def calculate_scenic_score(grid: List[List[int]], row: int, col: int) -> int:
    height = grid[row][col]
    rows = len(grid)
    cols = len(grid[0])

    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
        return 0

    left_count = 0
    for c in range(col - 1, -1, -1):
        left_count += 1
        if grid[row][c] >= height:
            break

    right_count = 0
    for c in range(col + 1, cols):
        right_count += 1
        if grid[row][c] >= height:
            break

    up_count = 0
    for r in range(row - 1, -1, -1):
        up_count += 1
        if grid[r][col] >= height:
            break

    down_count = 0
    for r in range(row + 1, rows):
        down_count += 1
        if grid[r][col] >= height:
            break

    return left_count * right_count * up_count * down_count


def solve_first_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    grid = parse_forest(lines)

    visible_count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if is_visible(grid, row, col):
                visible_count += 1

    elf.print_solution(1, visible_count)


def solve_second_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    grid = parse_forest(lines)

    max_score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            score = calculate_scenic_score(grid, row, col)
            max_score = max(max_score, score)

    elf.print_solution(2, max_score)


def main():
    parts, input_path = elf.parse_command_line()

    for part in parts:
        if part == 1:
            solve_first_part(input_path)
        elif part == 2:
            solve_second_part(input_path)


if __name__ == "__main__":
    main()
