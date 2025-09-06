import enum
import functools
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
import tomllib
from types import MappingProxyType
from typing import ClassVar

from ._defs import ROOT, SOLUTIONS_ROOT


class Lang(str, enum.Enum):
    PYTHON = "python"
    CPP = "cpp"
    GOLANG = "go"


LANG_TO_FILE_EXT = MappingProxyType(
    {
        Lang.PYTHON: ".py",
        Lang.CPP: ".cpp",
        Lang.GOLANG: ".go",
    }
)

assert len(Lang) == len(LANG_TO_FILE_EXT), "Not all registered languages have extension"
assert all(ext.startswith(".") for ext in LANG_TO_FILE_EXT.values()), (
    "Not all extensions start with a period"
)


def parse_compile_flags(root: Path) -> Sequence[str]:
    flags = root.joinpath("compile_flags.txt").read_text().splitlines()
    for idx, flag in enumerate(flags):
        if flag.startswith(prefix := "-I") and (
            include_path := flag.removeprefix(prefix)
        ).startswith("."):
            flags[idx] = f"-I{root.joinpath(include_path).resolve()}"
    return flags


@dataclass(kw_only=True)
class Command:
    EXECUTABLE_NAME: ClassVar[str] = "a.out"

    lang: Lang

    build_parts: Sequence[str] | None = None
    build_envs: Mapping[str, str] | None = None

    solve_parts: Sequence[str] | None = None
    solve_envs: Mapping[str, str] | None = None

    def resolve_build_args(self, main_path: Path) -> list[str]:
        if not self.build_parts:
            return []
        return [*self.pixi_parts, *self.build_parts, str(main_path)]

    def resolve_inference_args(
        self,
        *,
        main_path: Path,
        input_path: Path,
        part: int | None,
    ) -> list[str]:
        args: list[str] = []
        if self.solve_parts:
            assert main_path is not None, (
                f"Language {self.lang.value} run is expected to be run as interpreted, main path is required"
            )
            args.extend(self.pixi_parts)
            args.extend(self.solve_parts)
        args.extend(map(str, (main_path, "-i", input_path, "-p", part)))
        return args

    @property
    def pixi_parts(self) -> list[str]:
        out = ["pixi", "-q", "run"]
        if self.lang in self._pixi_environments:
            out.extend(("-e", self.lang.value))
        return out

    @functools.cached_property
    def _pixi_environments(self) -> frozenset[str]:
        return frozenset(tomllib.loads(ROOT.joinpath("pixi.toml").read_text())["environments"])


LANG_TO_COMMAND = MappingProxyType(
    {
        Lang.PYTHON: Command(
            lang=Lang.PYTHON,
            solve_parts=["python", "-OO"],
            solve_envs={"PYTHONPATH": str(SOLUTIONS_ROOT / Lang.PYTHON.value)},
        ),
        Lang.GOLANG: Command(
            lang=Lang.GOLANG,
            solve_parts=["go", "run"],
        ),
        Lang.CPP: Command(
            lang=Lang.CPP,
            build_parts=[
                "clang++",
                *parse_compile_flags(SOLUTIONS_ROOT / Lang.CPP.value),
                "-o",
                Command.EXECUTABLE_NAME,
            ],
            solve_parts=[f"./{Command.EXECUTABLE_NAME}"],
        ),
    }
)
