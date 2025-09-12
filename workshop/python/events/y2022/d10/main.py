#!/usr/bin/env python3

import elf
from typing import List, Tuple


def parse_instructions(lines: List[str]) -> List[Tuple[str, int]]:
    instructions = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if parts[0] == "noop":
            instructions.append(("noop", 0))
        elif parts[0] == "addx":
            instructions.append(("addx", int(parts[1])))
    return instructions


def execute_program(instructions: List[Tuple[str, int]]) -> List[int]:
    """Returns the value of X register at each cycle"""
    x = 1
    cycle_values = [x]

    for instruction, value in instructions:
        if instruction == "noop":
            cycle_values.append(x)
        elif instruction == "addx":
            cycle_values.append(x)
            cycle_values.append(x)
            x += value

    return cycle_values


def solve_first_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    instructions = parse_instructions(lines)
    cycle_values = execute_program(instructions)

    signal_sum = 0
    check_cycles = [20, 60, 100, 140, 180, 220]

    for cycle in check_cycles:
        if cycle < len(cycle_values):
            signal_strength = cycle * cycle_values[cycle]
            signal_sum += signal_strength

    elf.print_solution(1, signal_sum)


def solve_second_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    instructions = parse_instructions(lines)
    cycle_values = execute_program(instructions)

    crt_width = 40
    crt_height = 6
    screen = []

    for cycle in range(1, min(len(cycle_values), crt_width * crt_height + 1)):
        pixel_pos = (cycle - 1) % crt_width
        sprite_pos = cycle_values[cycle]

        if abs(pixel_pos - sprite_pos) <= 1:
            screen.append("#")
        else:
            screen.append(".")

        if cycle % crt_width == 0:
            screen.append("\n")

    output = "".join(screen).strip()
    elf.print_solution(2, "\n" + output)


def main():
    parts, input_path = elf.parse_command_line()

    for part in parts:
        if part == 1:
            solve_first_part(input_path)
        elif part == 2:
            solve_second_part(input_path)


if __name__ == "__main__":
    main()
