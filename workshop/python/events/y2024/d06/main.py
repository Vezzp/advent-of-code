from pathlib import Path
from typing import assert_never

import elf

type Grid = dict[Position, str]
type Position = complex
type Direction = complex

UP, DOWN, RIGHT, LEFT = (
    +0 - 1j,  # ↑
    +0 + 1j,  # ↓
    +1 + 0j,  # →
    -1 + 0j,  # ←
)

TURN_RULES = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


def parse_input(__p: Path, /) -> tuple[Grid, Position]:
    grid = {
        x + y * 1j: char
        for y, row in enumerate(elf.read_file_rows(__p))
        for x, char in enumerate(row)
    }

    for pos, char in grid.items():
        if char == "^":
            start_position = pos
            grid[pos] = "."
            break
    else:
        raise RuntimeError("Invalid map")

    return grid, start_position


def find_nonblocking_positions(
    grid: Grid, start_position: Position, start_direction: Direction
) -> set[Position]:
    direction = start_direction
    visited = {start_position}
    while True:
        match grid.get(next_pos := start_position + direction):
            case None:
                break
            case "#":
                direction = TURN_RULES[direction]
            case ".":
                visited.add(next_pos)
                start_position = next_pos
            case _:
                raise RuntimeError("Invalid map")
    return visited


def solve_first_part(__p: Path, /) -> None:
    grid, start_position = parse_input(__p)
    visited = find_nonblocking_positions(grid, start_position, UP)
    elf.print_solution(1, len(visited))


def solve_second_part(__p: Path, /) -> None:
    grid, start_position = parse_input(__p)
    visited = find_nonblocking_positions(grid, start_position, UP)
    solution = 0
    elf.print_solution(2, solution)


def main() -> None:
    parts, input = elf.parse_command_line()
    for part in parts:
        match part:
            case 1:
                solve_first_part(input)
            case 2:
                solve_second_part(input)
            case _:
                assert_never(part)


if __name__ == "__main__":
    main()
