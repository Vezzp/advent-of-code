import shutil

import typer
from loguru import logger

from ._langs import LANG_TO_FILE_EXT
from ._typer import CommonOpts
from ._utils import get_daily_present_root, get_daily_solution_root, get_elf_root, get_template_path


def init_handler(
    *,
    ctx: typer.Context,
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
    if solution_root.exists():
        logger.info(f"Daily solution root was already initialized: {solution_root}")
    else:
        solution_template_path = get_template_path(opts.lang)
        if not solution_template_path.exists():
            raise FileExistsError(f"Template path not found: {solution_template_path}")

        solution_root.mkdir(parents=True)
        shutil.copy(solution_template_path, solution_root / f"main{LANG_TO_FILE_EXT[opts.lang]}")
        logger.info(f"Initialized daily solution root: {solution_root}")
