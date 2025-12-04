from pathlib import Path
from typing import Literal

from ._defs import PRESENTS_ROOT, SOLUTIONS_ROOT
from ._langs import Lang


def get_daily_present_root(*, year: int, day: int) -> Path:
    return PRESENTS_ROOT.joinpath(f"y{year}", f"d{day:02d}")


def get_daily_solution_root(*, lang: Lang, year: int, day: int) -> Path:
    return get_lang_path(lang).joinpath("events", f"y{year}", f"d{day:02d}")


def get_elf_root(lang: Lang) -> Path:
    return get_lang_path(lang) / "elf"


def get_event_root(lang: Lang) -> Path:
    return get_lang_path(lang) / "events"


def get_lang_path(lang: Lang) -> Path:
    return SOLUTIONS_ROOT.joinpath(lang.value.lower())


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
