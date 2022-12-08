from __future__ import annotations

import argparse
import enum
import re
import importlib.util
import sys
from typing import TypedDict, cast
import warnings
from pathlib import Path

from typing_extensions import TypeAlias

__parent__ = Path(__file__).resolve().parent

PUZZLE_NAME_RE = re.compile(
    r"(?:---)?\s+Day\s+(?P<day>\d+):\s+(?P<name>.+)\s+(?:---)?"
)


Tree: TypeAlias = list["Tree"] | dict[str, "Tree"] | str


class ParsedPuzzleName(TypedDict):
    day: str
    name: str


def make_tree(root: Path, tree: Tree) -> None:
    match tree:
        case str():
            root.mkdir(parents=True, exist_ok=True)
            (root / tree).touch()

        case list():
            for subtree in tree:
                make_tree(root, subtree)

        case dict():
            for dirname, subtree in tree.items():
                make_tree(root / dirname, subtree)

        case _:
            raise TypeError(type(tree))


class Part(str, enum.Enum):
    ONE = "one"
    TWO = "two"


class Case(str, enum.Enum):
    TEST = "test"
    TASK = "task"


def setup(args: argparse.Namespace) -> None:
    if (match := PUZZLE_NAME_RE.match(args.name)) is None:
        raise RuntimeError()

    parsed_puzzle_name = cast(ParsedPuzzleName, match.groupdict())
    day = parsed_puzzle_name["day"]
    name = parsed_puzzle_name["name"]

    day_dpath = __parent__ / f"day_{day}_{name.lower().replace(' ', '_')}"

    msg_ph = f"Directory for day {day} ({name}) was {{}} set up"

    if day_dpath.exists():
        warnings.warn(msg_ph.format("already"))
        return

    make_tree(
        day_dpath,
        [
            "parser.py",
            "__init__.py",
            {
                "solution": [
                    "input.txt",
                    "test_input.txt",
                    "one.py",
                    "two.py",
                ]
            },
        ],
    )

    print(msg_ph.format("successfully"))


def solve(args: argparse.Namespace) -> None:
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


def prepare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser("solve", help="Solve puzzle per day")
    subparser.add_argument("-d", "--day", type=int, required=True)
    subparser.add_argument(
        "-p", "--part", type=str, choices=["one", "two"], required=True
    )
    subparser.add_argument(
        "-c", "--case", type=str, choices=["test", "task"], required=False, default=None
    )
    subparser.add_argument("-i", "--input", type=str, required=False, default=None)
    subparser.set_defaults(handler=solve)

    subparser = subparsers.add_parser("setup", help="Setup directory for daily puzzle")
    subparser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="Name of task copy pasted from the web site",
    )
    subparser.set_defaults(handler=setup)

    return parser


def main() -> None:
    parser = prepare_parser()
    args = parser.parse_args()
    args.handler(args)


main()
