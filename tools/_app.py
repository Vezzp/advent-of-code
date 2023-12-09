import _thread
import dataclasses
import enum
import functools
import inspect
import operator
import re
import selectors
import shutil
import subprocess
import sys
import threading
import unittest
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    ClassVar,
    Iterable,
    Literal,
    NotRequired,
    Optional,
    Self,
    TextIO,
    TypeAlias,
    TypedDict,
    cast,
)

import loguru
import typer

ROOT = Path(__file__).parent.parent
TEMPLATE_ROOT = ROOT / "tools" / "templates"

TEST_RE = re.compile(r"test_(?:p(?P<part>1|2)_)?(?P<idx>\d+)_(?P<type>in|out)")
SOLUTION_RE = re.compile(r"Part (?P<part>1|2) solution: (?P<answer>\w+)")

app = typer.Typer()


class ParsedTest(TypedDict):
    part: NotRequired[Literal["1", "2"] | None]
    idx: str
    type: Literal["in", "out"]


class ParsedSolution(TypedDict):
    part: Literal["1", "2"]
    answer: str


@dataclasses.dataclass(slots=True)
class TestCase:
    puzzle: Path | None = None
    answer: Path | None = None

    def __bool__(self) -> bool:
        return self.puzzle is not None and self.answer is not None


@dataclasses.dataclass
class ParsedPuzzleName:
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"(?:---\s*Day\s*)?(?P<day>\d+)?:?\s*(?P<name>.+\w)\s*(?:\s+---)?"
    )

    day: Optional[int]
    name: str

    def __post_init__(self) -> None:
        self.name = "_".join(self.name.lower().split())

    @classmethod
    def from_str(cls, __s: str, /) -> Self:
        if TYPE_CHECKING:

            class GroupDict(TypedDict):
                day: str
                name: str

        if (match := cls.PATTERN.match(__s)) is None:
            raise RuntimeError(
                f'Puzzle name "{__s}" does not match {cls.PATTERN.pattern}'
            )

        group_dict = cast("GroupDict", match.groupdict())
        out = cls(
            day=None if (day := group_dict.get("day")) is None else int(day),
            name=group_dict["name"],
        )
        return out


Part: TypeAlias = Annotated[
    Optional[int],
    typer.Option(
        "-p",
        "--part",
        help="Which part to solve. Leave blank for both parts.",
        min=1,
        max=2,
    ),
]


class Lang(str, enum.Enum):
    PYTHON = "py"
    CPP = "cpp"
    GOLANG = "go"


LANG_TO_CMD = {
    Lang.PYTHON: "python -OO",
    Lang.GOLANG: "go run",
}


@dataclasses.dataclass(kw_only=True, slots=True)
class CommonOpts:
    ATTRNAME: ClassVar[str] = "_common_opts_"

    year: Annotated[
        int,
        typer.Option("-y", "--year"),
    ] = datetime.now().year
    day: Annotated[
        int,
        typer.Option("-d", "--day"),
    ] = dataclasses.field(
        default=...,  # type: ignore
    )
    langs: Annotated[
        list[Lang],
        typer.Option("-l", "--lang"),
    ] = dataclasses.field(
        default=...,  # type: ignore
    )


@functools.wraps(app.command)
def command(*args, **kwargs):
    def decorator(__f):
        @functools.wraps(__f)
        def wrapper(*__args, **__kwargs):
            assert len(__args) == 0
            __kwargs = _patch_command_wrapper_kwargs(**__kwargs)
            return __f(**__kwargs)

        _patch_command_signature(wrapper)

        return app.command(*args, **kwargs)(wrapper)

    return decorator


def _patch_command_wrapper_kwargs(**kwargs) -> dict[str, Any]:
    if (ctx := kwargs.get("ctx")) is None:
        raise RuntimeError("Context should be provided")

    common_opts_params = {}
    for field in dataclasses.fields(CommonOpts):
        common_opts_params[field.name] = kwargs.pop(field.name)
    common_opts = CommonOpts(**common_opts_params)

    setattr(ctx, CommonOpts.ATTRNAME, common_opts)

    return {"ctx": ctx, **kwargs}


def _patch_command_signature(__w: Callable, /) -> None:
    sig = inspect.signature(__w)
    new_parameters = sig.parameters.copy()
    for field in dataclasses.fields(CommonOpts):
        new_parameters[field.name] = inspect.Parameter(
            name=field.name,
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=field.default,
            annotation=field.type,
        )
    new_sig = sig.replace(parameters=tuple(new_parameters.values()))
    setattr(__w, "__signature__", new_sig)


@command("setup", help="Setup directory and draft template for daily puzzle")
def setup_handler(
    *, ctx: typer.Context, name: Annotated[str, typer.Option("-n", "--name")]
) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    puzzle_name = ParsedPuzzleName.from_str(name.strip())
    day_root = ROOT.joinpath(
        "src",
        f"year_{opts.year}",
        f"day_{opts.day}_{puzzle_name.name}",
    )
    day_root.mkdir(parents=True, exist_ok=True)
    for filename in (
        "input.txt",
        "test_p1_1_in.txt",
        "test_p1_1_out.txt",
        "test_p2_1_in.txt",
        "test_p2_1_out.txt",
    ):
        day_root.joinpath(filename).touch()

    for lang in opts.langs:
        lang_root = day_root / f"lang_{lang.value}"
        entrypoint_name = f"main.{lang.value}"
        solution_fpath = lang_root / entrypoint_name
        if solution_fpath.exists():
            loguru.logger.warning(
                f"Solution/ solution draft for Advent-of-Code {opts.year}, day {puzzle_name.day}, "
                f"implemented in {lang.name.lower()}, already exists at {solution_fpath}"
            )
        else:
            loguru.logger.info(
                f"Solution draft for Advent-of-Code {opts.year}, day {puzzle_name.day}, "
                f"implemented in {lang.name.lower()}, successfully created at {solution_fpath}"
            )
            solution_fpath.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                TEMPLATE_ROOT / entrypoint_name,
                solution_fpath,
            )


@command("solve")
def solve_handler(*, ctx: typer.Context, part: Part = None) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    day_root = get_day_root(opts)
    puzzle_fpath = day_root / "input.txt"

    for lang, root in iter_lang_roots(opts, day_root):
        run_inference(root, lang, part, puzzle_fpath)


@command("test")
def test_handler(
    *,
    ctx: typer.Context,
    part: Part = None,
    suppress_stdout: Annotated[
        bool, typer.Option("-s/-S", "--stdout/--no-stdout")
    ] = False,
) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    day_root = get_day_root(opts)

    parts = resolve_parts(part)
    tests = collect_tests(day_root)

    for lang, lang_root in iter_lang_roots(opts, day_root):

        class TextSubtestTestResult(unittest.TextTestResult):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                # NOTE(vshlenskii): Exclude initial test from countF.
                self.testsRun = -1

            def addSubTest(self, test, subtest, outcome):
                super().addSubTest(test, subtest, outcome)
                self.testsRun += 1

        class TestCase(unittest.TestCase):
            def test(self) -> None:
                for test_idx, test_part, test_case in tests:
                    if test_part not in parts:
                        continue

                    for fpath_ in (test_case.puzzle, test_case.answer):
                        if fpath_ is None or not fpath_.exists():
                            raise RuntimeError(f"{fpath_} should exist")

                    assert test_case.answer is not None
                    assert test_case.puzzle is not None

                    answer_lines = test_case.answer.read_text().splitlines()
                    if len(answer_lines) == 0:
                        raise RuntimeError(f"{test_case.answer} is empty")

                    answer = answer_lines[0]

                    with self.subTest(f"{test_idx = } {test_part = }"):
                        solution = run_inference(
                            lang_root,
                            lang,
                            test_part,
                            test_case.puzzle,
                            suppress_stdout=suppress_stdout,
                        )[0]
                        self.assertEqual(solution["answer"], answer)

        test_runner = unittest.TextTestRunner(
            stream=sys.stdout,
            resultclass=TextSubtestTestResult,
        )
        test_runner.run(unittest.makeSuite(TestCase))


def get_day_root(opts: CommonOpts, /) -> Path:
    year_root = ROOT.joinpath("src", f"year_{opts.year}")
    if not year_root.exists():
        raise RuntimeError(f"Year {opts.year} was not setup")

    day_root = next(iter(year_root.glob(f"day_{opts.day}*")))
    if not day_root.exists():
        raise RuntimeError(f"Day {opts.day} was not setup")

    return day_root


def iter_lang_roots(
    opts: CommonOpts,
    /,
    day_root: Path | None = None,
) -> Iterable[tuple[Lang, Path]]:
    if day_root is None:
        day_root = get_day_root(opts)

    for lang in opts.langs:
        lang_root = day_root / f"lang_{lang.value}"
        if not lang_root.exists():
            raise RuntimeError(f"Language {lang.value} was not setup")

        yield (lang, lang_root)


def run_inference(
    root: Path, lang: Lang, part: int | None, path: Path, suppress_stdout: bool = False
) -> list[ParsedSolution]:
    entrypoint = root / f"main.{lang.value}"

    parsed_solutions: list[ParsedSolution] = []
    parts = resolve_parts(part)

    # https://gist.github.com/nawatts/e2cdca610463200c12eac2a14efc0bfb
    def stdout_handler(stream: TextIO) -> None:
        line = stream.readline()
        if not suppress_stdout:
            sys.stdout.write(line)
        if (match := SOLUTION_RE.match(line)) is None:
            return None

        parsed_solution = cast(ParsedSolution, match.groupdict())
        parsed_solutions.append(parsed_solution)

    proc = subprocess.Popen(
        (
            cmd := f"pixi -q run {LANG_TO_CMD[lang]} {entrypoint} -p {part} {path}"
        ).split(),
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    selector = selectors.DefaultSelector()
    assert proc.stdout is not None
    selector.register(proc.stdout, selectors.EVENT_READ, stdout_handler)

    def handle(timeout: float | None = None) -> None:
        for key, _ in selector.select(timeout):
            key.data(key.fileobj)

    while proc.poll() is None:
        handle()

    if (return_code := proc.wait()) != 0:
        selector.close()
        raise subprocess.CalledProcessError(
            return_code,
            cmd,
            stderr=f"{proc.stderr}",
        )

    # NOTE(vshlenskii): Two seconds must be enough to read remaining lines.
    timer = threading.Timer(2, _thread.interrupt_main)
    timer.start()
    try:
        while len(parsed_solutions) != len(parts):
            handle()
    finally:
        timer.cancel()
    selector.close()

    return parsed_solutions


def collect_tests(root: Path, /) -> list[tuple[str, Literal[1, 2], TestCase]]:
    idx_to_parsed_test: dict[str, list[tuple[ParsedTest, Path]]] = defaultdict(list)

    for fpath in root.glob("*.txt"):
        if (match := TEST_RE.match(fpath.stem)) is None:
            continue
        parsed_test = cast(ParsedTest, match.groupdict())
        idx_to_parsed_test[parsed_test["idx"]].append((parsed_test, fpath))

    grouped_tests: dict[str, dict[Literal[1, 2], TestCase]] = defaultdict(
        lambda: defaultdict(TestCase)
    )
    for idx, tests in idx_to_parsed_test.items():
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
                        raise RuntimeError(f"Test type {test['type']} is not supported")

    out: list[tuple[str, Literal[1, 2], TestCase]] = sorted(
        (
            (idx, part, test)
            for idx, tests in grouped_tests.items()
            for part, test in tests.items()
            if test
        ),
        key=operator.itemgetter(0),
    )

    return out


def resolve_parts(part: int | None | str, /) -> tuple[Literal[1, 2], ...]:
    match part:
        case None:
            parts = (1, 2)
        case "1" | 1:
            parts = (1,)
        case "2" | 2:
            parts = (2,)
        case _:
            raise RuntimeError(f"Part {part} is not supported")
    return parts
