import shutil
from typing import Annotated

import typer
from loguru import logger

from ._commands import LANG_TO_COMMAND
from ._typer import CommonOpts
from ._utils import get_daily_present_root, get_daily_solution_root, get_elf_root


def init_handler(
    *,
    ctx: typer.Context,
    force: Annotated[bool, typer.Option(help="Force day directory initialization")] = False,
) -> None:
    opts = getattr(ctx, CommonOpts.ATTRNAME, ...)
    assert isinstance(opts, CommonOpts), f"Typer context does not contain expected options: {opts}"

    elf_root = get_elf_root(opts.lang)
    if not elf_root.exists():
        logger.trace(f"Elf root {elf_root} does not exist")

    present_root = get_daily_present_root(year=opts.year, day=opts.day)
    if present_root.exists():
        logger.info(f"Daily present root was already initialized: {present_root}")
    else:
        present_root.mkdir(parents=True)
        for filename in (
            "input.txt",
            "test_p1_n1_in.txt",
            "test_p1_n1_out.txt",
            "test_p2_n1_in.txt",
            "test_p2_n1_out.txt",
        ):
            present_root.joinpath(filename).touch()

        logger.info(f"Initialized daily present root: {present_root}")

    solution_root = get_daily_solution_root(lang=opts.lang, year=opts.year, day=opts.day)
    if solution_root.exists() and not force:
        logger.info(
            f"Daily solution root was already initialized: {solution_root}. Use --force to force recreate"
        )
    else:
        shutil.rmtree(solution_root, ignore_errors=True)  # noqa: F821
        solution_root = LANG_TO_COMMAND[opts.lang].day_initializer(year=opts.year, day=opts.day)
        logger.info(f"Initialized daily solution root: {solution_root}")
