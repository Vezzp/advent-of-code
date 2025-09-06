import operator
import re
import sys
import unittest
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NotRequired, TypedDict, assert_never, cast, override

import typer

from ._langs import LANG_TO_COMMAND
from ._solver import solve_puzzle
from ._typer import CommonOpts, Part
from ._utils import get_daily_entrypoint, get_daily_present_root, resolve_parts

TEST_RE = re.compile(r"test_(?:p(?P<part>1|2)_)?n(?P<idx>\d+)_(?P<type>in|out)")


class ParsedTestCaseFilename(TypedDict):
    idx: str
    part: NotRequired[Literal["1", "2"] | None]
    type: Literal["in", "out"]


@dataclass(slots=True)
class TestCase:
    puzzle: Path | None = None
    answer: Path | None = None

    def __bool__(self) -> bool:
        return self.puzzle is not None and self.answer is not None


def test_handler(
    *,
    ctx: typer.Context,
    part: Part = None,
) -> None:
    opts = getattr(ctx, CommonOpts.ATTRNAME, ...)
    assert isinstance(opts, CommonOpts), f"Typer context does not contain expected options: {opts}"

    def make_test_case() -> type[unittest.TestCase]:
        tests = collect_tests(get_daily_present_root(year=opts.year, day=opts.day))
        parts = resolve_parts(part)

        class TestCase(unittest.TestCase):
            def test(self) -> None:
                command = LANG_TO_COMMAND[opts.lang]
                for test_idx, test_part, test_case in tests:
                    if test_part not in parts:
                        continue

                    for fpath_ in (test_case.puzzle, test_case.answer):
                        if fpath_ is None or not fpath_.exists():
                            raise FileExistsError(f"{fpath_} should exist")

                    assert test_case.answer is not None
                    assert test_case.puzzle is not None

                    answer_lines = test_case.answer.read_text().splitlines()
                    if len(answer_lines) == 0:
                        raise FileExistsError(f"{test_case.answer} is empty")

                    answer = answer_lines[0]

                    with self.subTest(f"{test_idx = } {test_part = }"):
                        solution = solve_puzzle(
                            command=command,
                            input_path=test_case.puzzle,
                            main_path=get_daily_entrypoint(
                                lang=opts.lang, year=opts.year, day=opts.day
                            ),
                            part=test_part,
                        )[0]
                        self.assertEqual(solution["answer"], answer)  # noqa: PT009

        return TestCase

    class TextSubtestTestResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            # NOTE(vshlenskii): Exclude initial test from count.
            self.testsRun = -1

        @override
        def addSubTest(self, test, subtest, outcome):
            super().addSubTest(test, subtest, outcome)
            self.testsRun += 1

    test_runner = unittest.TextTestRunner(
        stream=sys.stdout,
        resultclass=TextSubtestTestResult,
    )
    test_runner.run(unittest.TestLoader().loadTestsFromTestCase(make_test_case()))


def collect_tests(root: Path) -> list[tuple[int, Literal[1, 2], TestCase]]:
    idx_to_parsed_test_case_filename: dict[str, list[tuple[ParsedTestCaseFilename, Path]]] = (
        defaultdict(list)
    )
    for fpath in root.glob("*.txt"):
        if (match := TEST_RE.match(fpath.stem)) is None:
            continue
        parsed_test = cast(ParsedTestCaseFilename, match.groupdict())
        idx_to_parsed_test_case_filename[parsed_test["idx"]].append((parsed_test, fpath))

    grouped_tests: dict[str, dict[Literal[1, 2], TestCase]] = defaultdict(
        lambda: defaultdict(TestCase)
    )
    for idx, tests in idx_to_parsed_test_case_filename.items():
        for test, fpath in tests:
            parts = resolve_parts(test.get("part"))
            for part in parts:
                test_case = grouped_tests[idx][part]
                match test["type"]:
                    case "in":
                        test_case.puzzle = fpath
                    case "out":
                        test_case.answer = fpath
                    case _:
                        assert_never(test["type"])

    return sorted(
        [
            (int(idx), part, test)
            for idx, tests in grouped_tests.items()
            for part, test in tests.items()
            if test
        ],
        key=operator.itemgetter(0, 1),
    )
