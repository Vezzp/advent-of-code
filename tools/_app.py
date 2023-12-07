import dataclasses
import enum
import functools
import inspect
import subprocess
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    ClassVar,
    Optional,
    cast,
)

import loguru
import typer
from typing_extensions import Self, TypedDict


ROOT = Path(__file__).parent.parent
TEMPLATE_ROOT = ROOT / "tools" / "templates"


@dataclasses.dataclass
class ParsedPuzzleName:
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"(?:---\s*)?Day\s+(?P<day>\d+):\s*(?P<name>.+\w)\s*(?:\s+---)?"
    )

    day: int
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
            day=int(group_dict["day"]),
            name=group_dict["name"],
        )
        return out


app = typer.Typer()


class Lang(str, enum.Enum):
    PYTHON = "py"
    CPP = "cpp"
    GOLANG = "go"


@dataclasses.dataclass(kw_only=True, slots=True)
class CommonOpts:
    ATTRNAME: ClassVar[str] = "_common_opts_"

    year: Annotated[
        int,
        typer.Option("-y", "--year"),
    ] = datetime.now().year
    langs: Annotated[
        list[Lang],
        typer.Option("-l", "--lang"),
    ] = dataclasses.field(
        default=...,  # type: ignore
    )


type DayOption = Annotated[
    Optional[int],
    typer.Option("-d", "--day"),
]


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
    *,
    ctx: typer.Context,
    name: Annotated[str, typer.Option("-n", "--name")],
) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    puzzle_name = ParsedPuzzleName.from_str(name.strip())
    for lang in opts.langs:
        solution_root = ROOT.joinpath(
            "src",
            f"year_{opts.year}",
            f"day_{puzzle_name.day}_{puzzle_name.name}",
            f"lang_{lang.value}",
        )
        solution_name = f"main.{lang.value}"
        solution_fpath = solution_root / solution_name
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
                TEMPLATE_ROOT / solution_name,
                solution_fpath,
            )
            solution_root.joinpath("input.txt").touch()


@command("solve")
def solve(
    *,
    ctx: typer.Context,
    day: Annotated[str, typer.Option("-d", "--day")],
    part: Annotated[
        Optional[int],
        typer.Option(
            "-p",
            "--part",
        ),
    ] = None,
) -> None:
    opts: CommonOpts = getattr(ctx, CommonOpts.ATTRNAME)
    year_root = ROOT.joinpath("src", f"year_{opts.year}")
    day_root = next(iter(year_root.glob(f"day_{day}*")))

    for lang in opts.langs:
        lang_root = day_root / f"lang_{lang.value}"

        input_fpath = lang_root / "input.txt"
        solution_fpath = lang_root / f"main.{lang.value}"
        subprocess.call(
            f"pixi run go run {solution_fpath} -p {part} {input_fpath}",
            shell=True,
        )


# @app.command("test")
# def test():
#     ...
