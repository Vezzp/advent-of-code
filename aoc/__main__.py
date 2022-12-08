from __future__ import annotations

import argparse
import enum
import importlib.util
import sys
from pathlib import Path

__parent__ = Path(__file__).resolve().parent


class Part(str, enum.Enum):
    ONE = "one"
    TWO = "two"


class Case(str, enum.Enum):
    TEST = "test"
    TASK = "task"


def prepare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", type=int, required=True)
    parser.add_argument("-p", "--part", type=str, choices=["one", "two"], required=True)
    parser.add_argument(
        "-c", "--case", type=str, choices=["test", "task"], required=False, default=None
    )
    parser.add_argument("-i", "--input", type=str, required=False, default=None)

    return parser


def main() -> None:
    parser = prepare_parser()
    args = parser.parse_args()

    day_dpath = next(iter((__parent__.glob(f"day_{args.day}*"))))

    spec = importlib.util.spec_from_file_location(
        (mname := "solver"),
        day_dpath / "solution" / f"{args.part}.py",
    )
    assert spec is not None

    solver = importlib.util.module_from_spec(spec)
    sys.modules[mname] = solver

    assert spec.loader is not None
    spec.loader.exec_module(solver)

    solve = solver.solve

    match args.case:
        case "task":
            input_fpath = day_dpath / "solution" / "input.txt"

        case "test":
            from aoc.utils import run_tests

            run_tests(
                solve, (day_dpath / "solution" / "test_input.txt", solver.TEST_OUTPUT)
            )

            return

        case _:
            assert args.input is not None
            input_fpath = Path(args.input)

    with input_fpath.open() as fin:
        print(solve(fin))


main()
