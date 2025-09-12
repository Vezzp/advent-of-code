#!/usr/bin/env python3

import elf
from typing import List, Tuple, Set


def parse_moves(lines: List[str]) -> List[Tuple[str, int]]:
    moves = []
    for line in lines:
        line = line.strip()
        if line:
            direction, steps = line.split()
            moves.append((direction, int(steps)))
    return moves


def sign(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


def move_head(head: Tuple[int, int], direction: str) -> Tuple[int, int]:
    x, y = head
    if direction == "R":
        return (x + 1, y)
    elif direction == "L":
        return (x - 1, y)
    elif direction == "U":
        return (x, y + 1)
    elif direction == "D":
        return (x, y - 1)
    return head


def follow(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    hx, hy = head
    tx, ty = tail

    dx = hx - tx
    dy = hy - ty

    if abs(dx) <= 1 and abs(dy) <= 1:
        return tail

    return (tx + sign(dx), ty + sign(dy))


def simulate_rope(moves: List[Tuple[str, int]], rope_length: int) -> int:
    rope = [(0, 0)] * rope_length
    visited = set()
    visited.add(rope[-1])

    for direction, steps in moves:
        for _ in range(steps):
            rope[0] = move_head(rope[0], direction)

            for i in range(1, rope_length):
                rope[i] = follow(rope[i - 1], rope[i])

            visited.add(rope[-1])

    return len(visited)


def solve_first_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    moves = parse_moves(lines)
    result = simulate_rope(moves, 2)
    elf.print_solution(1, result)


def solve_second_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    moves = parse_moves(lines)
    result = simulate_rope(moves, 10)
    elf.print_solution(2, result)


def main():
    parts, input_path = elf.parse_command_line()

    for part in parts:
        if part == 1:
            solve_first_part(input_path)
        elif part == 2:
            solve_second_part(input_path)


if __name__ == "__main__":
    main()
