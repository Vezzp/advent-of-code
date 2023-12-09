import dataclasses
import enum
import functools
import inspect
import re
import shutil
import subprocess
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
    TypeAlias,
    TypedDict,
    cast,
)

import loguru
import typer

ROOT = Path(__file__).parent.parent
TEMPLATE_ROOT = ROOT / "tools" / "templates"


TEST_RE = re.compile(r"test_(?:p(?P<part>1|2)_)?(?P<idx>\d+)_(?P<type>in|out)")


class ParsedTest(TypedDict):
    part: NotRequired[Literal["1", "2"] | None]
    idx: str
    type: Literal["in", "out"]


@dataclasses.dataclass(slots=True)
class TestCase:
    puzzle: Path | None = None
    solution: Path | None = None

    def __bool__(self) -> bool:
        return self.puzzle is not None and self.solution is not None


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


app = typer.Typer()


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
def setup(
    *, ctx: typer.Context, name: Annotated[str, typer.Option("-n", "--name")]
) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    puzzle_name = ParsedPuzzleName.from_str(name.strip())
    day_root = ROOT.joinpath(
        "src",
        f"year_{opts.year}",
        f"day_{opts.day}_{puzzle_name.name}",
    )
    day_root.joinpath("input.txt").touch()

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
def solve(*, ctx: typer.Context, part: Part = None) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    day_root = get_day_root(opts)
    puzzle_fpath = day_root / "input.txt"

    for lang, root in iter_lang_roots(opts, day_root):
        run_inference(root, lang, part, puzzle_fpath)


@command("test")
def test(*, ctx: typer.Context, part: Part = None) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    day_root = get_day_root(opts)

    tests = collect_tests(day_root)


def get_day_root(opts: CommonOpts, /) -> Path:
    year_root = ROOT.joinpath("src", f"year_{opts.year}")
    if not year_root.exists():
        raise RuntimeError(f"Year {opts.year} was not setup")

    day_root = next(iter(year_root.glob(f"day_{opts.day}*")))
    if not day_root.exists():
        raise RuntimeError(f"Day {opts.day} was not setup")

    return day_root


def iter_lang_roots(
    opts: CommonOpts, /, day_root: Path | None = None
) -> Iterable[tuple[Lang, Path]]:
    if day_root is None:
        day_root = get_day_root(opts)

    for lang in opts.langs:
        lang_root = day_root / f"lang_{lang.value}"
        if not lang_root.exists():
            raise RuntimeError(f"Language {lang.value} was not setup")

        yield (lang, lang_root)


def run_inference(root: Path, lang: Lang, part: int | None, path: Path) -> None:
    entrypoint = root / f"main.{lang.value}"
    subprocess.check_call(
        f"pixi run {LANG_TO_CMD[lang]} {entrypoint} -p {part} {path}",
        shell=True,
    )


def collect_tests(root: Path, /) -> dict[str, dict[Literal[1, 2], TestCase]]:
    idx_to_parsed_test: dict[str, list[tuple[ParsedTest, Path]]] = defaultdict(list)

    for fpath in root.glob("*.txt"):
        if (match := TEST_RE.match(fpath.stem)) is None:
            continue
        parsed_test = cast(ParsedTest, match.groupdict())
        idx_to_parsed_test[parsed_test["idx"]].append((parsed_test, fpath))

    out: dict[str, dict[Literal[1, 2], TestCase]] = defaultdict(
        lambda: defaultdict(TestCase)
    )
    for idx, tests in idx_to_parsed_test.items():
        for test, fpath in tests:
            match part := test.get("test"):
                case None:
                    parts = (1, 2)
                case "1":
                    parts = (1,)
                case "2":
                    parts = (2,)
                case _:
                    raise RuntimeError(f"Part {part} is not supported")

            for part in parts:
                test_case = out[idx][part]
                match test["type"]:
                    case "in":
                        test_case.puzzle = fpath
                    case "out":
                        test_case.solution = fpath
                    case _:
                        raise RuntimeError(f"Test type {test['type']} is not supported")

    print(out)

    return out
