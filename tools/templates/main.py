from pathlib import Path

import jogtrot


def solve_first_part(__p: Path, /) -> None:
    solution = f"Unimplemented. No solution for {__p!s}"
    jogtrot.print_solution(1, solution)


def solve_second_part(__p: Path, /) -> None:
    solution = f"Unimplemented. No solution for {__p!s}"
    jogtrot.print_solution(2, solution)


def main() -> None:
    parts, input = jogtrot.parse_command_line()
    for part in parts:
        match part:
            case 1:
                solve_first_part(input)
            case 2:
                solve_second_part(input)
            case _:
                raise RuntimeError(f"Part {part} is not supported")


if __name__ == "__main__":
    main()
