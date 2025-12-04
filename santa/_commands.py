import functools
import os
import shutil
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import ClassVar, Protocol, TypedDict

import tomli_w

from ._defs import ROOT, SOLUTIONS_ROOT
from ._langs import LANG_TO_FILE_EXT, Lang
from ._utils import get_daily_solution_root, get_event_root

TEMPLATE_PREFIX = "template"


class PopenOpts(TypedDict):
    cmd: Sequence[str]
    env: Mapping[str, str] | None
    cwd: Path | None


class PopenBuildOptsCtor(Protocol):
    def __call__(self, *, year: int, day: int) -> PopenOpts: ...


class PopenSolveOptsCtor(Protocol):
    def __call__(self, *, year: int, day: int, part: int | None, input_path: Path) -> PopenOpts: ...


class DayInitializer(Protocol):
    def __call__(self, *, year: int, day: int) -> Path: ...


@dataclass(kw_only=True)
class Command:
    EXECUTABLE_NAME: ClassVar[str] = "a.out"

    lang: Lang

    day_initializer: DayInitializer
    build_popen_opts_ctor: PopenBuildOptsCtor | None
    solve_popen_opts_ctor: PopenSolveOptsCtor

    def resolve_build_popen_opts(self, *, year: int, day: int) -> PopenOpts:
        assert self.build_popen_opts_ctor is not None, "build_popen_opts_ctor is required"
        opts = self.build_popen_opts_ctor(year=year, day=day)
        return self._extend_opts_with_pixi_extras(opts)

    def resolve_solve_popen_opts(
        self, *, year: int, day: int, part: int | None, input_path: Path
    ) -> PopenOpts:
        opts = self.solve_popen_opts_ctor(year=year, day=day, part=part, input_path=input_path)
        return self._extend_opts_with_pixi_extras(opts)

    def _extend_opts_with_pixi_extras(self, opts: PopenOpts, /) -> PopenOpts:
        pixi_extra_cmd_parts = ["pixi", "-q", "run"]
        if self.lang.value in self._pixi_environments:
            pixi_extra_cmd_parts.extend(("-e", self.lang.value))
        return {
            "cmd": [*pixi_extra_cmd_parts, *opts["cmd"]],
            "env": opts["env"],
            "cwd": opts["cwd"],
        }

    @functools.cached_property
    def _pixi_environments(self) -> frozenset[str]:
        return frozenset(tomllib.loads(ROOT.joinpath("pixi.toml").read_text())["environments"])


# =====
# Python
# =====


def construct_python_solve_popen_opts(
    *, year: int, day: int, part: int | None, input_path: Path
) -> PopenOpts:
    lang = Lang.PYTHON
    daily_root = get_daily_solution_root(lang=lang, year=year, day=day)
    main_path = daily_root.joinpath(f"main{LANG_TO_FILE_EXT[lang]}")
    return {
        "cmd": ["python", "-OO", str(main_path), *(_resolve_solve_input_args(part, input_path))],
        "env": os.environ | {"PYTHONPATH": str(SOLUTIONS_ROOT / Lang.PYTHON.value)},
        "cwd": SOLUTIONS_ROOT / lang.value,
    }


def python_day_initializer(*, year: int, day: int) -> Path:
    return _simple_main_template_day_initializer(lang=Lang.PYTHON, year=year, day=day)


# =====
# Golang
# =====


def construct_golang_solve_popen_opts(
    *, year: int, day: int, part: int | None, input_path: Path
) -> PopenOpts:
    lang = Lang.GOLANG
    daily_root = get_daily_solution_root(lang=lang, year=year, day=day)
    main_path = daily_root.joinpath(f"main{LANG_TO_FILE_EXT[lang]}")
    return {
        "cmd": ["go", "run", str(main_path), *(_resolve_solve_input_args(part, input_path))],
        "env": None,
        "cwd": SOLUTIONS_ROOT / lang.value,
    }


def golang_day_initializer(*, year: int, day: int) -> Path:
    return _simple_main_template_day_initializer(lang=Lang.GOLANG, year=year, day=day)


# =====
# C++
# =====


def construct_cpp_build_popen_opts(*, year: int, day: int) -> PopenOpts:
    def parse_compile_flags(root: Path) -> Sequence[str]:
        flags = root.joinpath("compile_flags.txt").read_text().splitlines()
        for idx, flag in enumerate(flags):
            if flag.startswith(prefix := "-I") and (
                include_path := flag.removeprefix(prefix)
            ).startswith("."):
                flags[idx] = f"-I{root.joinpath(include_path).resolve()}"
        return flags

    lang = Lang.CPP
    daily_root = get_daily_solution_root(lang=lang, year=year, day=day)
    main_path = daily_root.joinpath(f"main{LANG_TO_FILE_EXT[lang]}")
    return {
        "cmd": [
            "clang++",
            *parse_compile_flags(SOLUTIONS_ROOT / lang.value),
            "-o",
            Command.EXECUTABLE_NAME,
            str(main_path),
        ],
        "env": None,
        "cwd": SOLUTIONS_ROOT / lang.value,
    }


def construct_cpp_solve_popen_opts(
    *, year: int, day: int, part: int | None, input_path: Path
) -> PopenOpts:
    _ = year
    _ = day
    return {
        "cmd": [f"./{Command.EXECUTABLE_NAME}", *(_resolve_solve_input_args(part, input_path))],
        "env": None,
        "cwd": SOLUTIONS_ROOT / Lang.CPP.value,
    }


def cpp_day_initializer(*, year: int, day: int) -> Path:
    return _simple_main_template_day_initializer(lang=Lang.CPP, year=year, day=day)


# =====
# Rust
# =====


def construct_rust_solve_popen_opts(
    *, year: int, day: int, part: int | None, input_path: Path
) -> PopenOpts:
    lang = Lang.RUST
    daily_root = get_daily_solution_root(lang=lang, year=year, day=day)
    return {
        "cmd": [
            "cargo",
            "run",
            "--release",
            "--",
            *(_resolve_solve_input_args(part, input_path)),
        ],
        "env": None,
        "cwd": daily_root,
    }


def rust_day_initializer(*, year: int, day: int) -> Path:
    lang = Lang.RUST
    solution_root = get_daily_solution_root(lang=lang, year=year, day=day)
    template_path = get_event_root(lang) / TEMPLATE_PREFIX
    if not template_path.exists():
        raise FileExistsError(f"Template path not found: {template_path}")
    solution_root.mkdir(parents=True)
    shutil.copytree(template_path, solution_root, dirs_exist_ok=True)

    cargo_toml_path = solution_root.joinpath("Cargo.toml")
    cargo_toml_data = tomllib.loads(cargo_toml_path.read_text())
    cargo_toml_data["package"]["name"] = f"aoc-{year:04}-{day:02}"
    cargo_toml_data["dependencies"]["elf"]["path"] = "../../../elf"
    cargo_toml_path.write_text(tomli_w.dumps(cargo_toml_data))

    return solution_root


COMMANDS = (
    Command(
        lang=Lang.PYTHON,
        day_initializer=python_day_initializer,
        build_popen_opts_ctor=None,
        solve_popen_opts_ctor=construct_python_solve_popen_opts,
    ),
    Command(
        lang=Lang.GOLANG,
        day_initializer=golang_day_initializer,
        build_popen_opts_ctor=None,
        solve_popen_opts_ctor=construct_golang_solve_popen_opts,
    ),
    Command(
        lang=Lang.CPP,
        day_initializer=cpp_day_initializer,
        build_popen_opts_ctor=construct_cpp_build_popen_opts,
        solve_popen_opts_ctor=construct_cpp_solve_popen_opts,
    ),
    Command(
        lang=Lang.RUST,
        day_initializer=rust_day_initializer,
        build_popen_opts_ctor=None,
        solve_popen_opts_ctor=construct_rust_solve_popen_opts,
    ),
)

LANG_TO_COMMAND = MappingProxyType({command.lang: command for command in COMMANDS})


def _resolve_solve_input_args(part: int | None, input_path: Path) -> Sequence[str]:
    out = ["-i", str(input_path)]
    if part is not None:
        out.extend(["-p", str(part)])
    return out


def _simple_main_template_day_initializer(*, lang: Lang, year: int, day: int) -> Path:
    template_path = get_event_root(lang) / f"{TEMPLATE_PREFIX}{LANG_TO_FILE_EXT[lang]}"
    if not template_path.exists():
        raise FileExistsError(f"Template path not found: {template_path}")
    solution_root = get_daily_solution_root(lang=lang, year=year, day=day)
    solution_root.mkdir(parents=True)
    shutil.copy(template_path, solution_root / f"main{LANG_TO_FILE_EXT[lang]}")
    return solution_root
