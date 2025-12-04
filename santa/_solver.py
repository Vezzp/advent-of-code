import _thread
import re
import selectors
import subprocess
import sys
import threading
from pathlib import Path
from typing import Literal, TextIO, TypedDict, cast

import loguru
import typer

from ._langs import Lang
from ._commands import LANG_TO_COMMAND
from ._typer import CommonOpts, Part
from ._utils import get_daily_present_root, resolve_parts


class ParsedSolution(TypedDict):
    part: Literal["1", "2"]
    answer: str


SOLUTION_RE = re.compile(r"Part (?P<part>1|2) solution: (?P<answer>\w+)")


def solve_handler(*, ctx: typer.Context, part: Part = None) -> None:
    opts = getattr(ctx, CommonOpts.ATTRNAME, ...)
    assert isinstance(opts, CommonOpts), f"Typer context does not contain expected options: {opts}"
    solve_puzzle(
        lang=opts.lang,
        year=opts.year,
        day=opts.day,
        part=part,
        input_path=get_daily_present_root(year=opts.year, day=opts.day) / "input.txt",
    )


def solve_puzzle(
    *,
    lang: Lang,
    year: int,
    day: int,
    part: int | None = None,
    input_path: Path,
    suppress_stdout: bool = False,
) -> list[ParsedSolution]:
    parsed_solutions: list[ParsedSolution] = []

    # https://gist.github.com/nawatts/e2cdca610463200c12eac2a14efc0bfb
    def stdout_handler(stream: TextIO) -> None:
        line = stream.readline()
        if not suppress_stdout:
            sys.stdout.write(line)
        if (match := SOLUTION_RE.match(line)) is None:
            return
        parsed_solution = cast(ParsedSolution, match.groupdict())
        parsed_solutions.append(parsed_solution)

    command = LANG_TO_COMMAND[lang]
    if command.build_popen_opts_ctor is not None:
        build_popen_opts = command.resolve_build_popen_opts(year=year, day=day)
        loguru.logger.info("Building ...")
        loguru.logger.info(build_popen_opts["cmd"])
        subprocess.check_call(
            build_popen_opts["cmd"],
            env=build_popen_opts["env"],
            cwd=build_popen_opts["cwd"],
        )
        loguru.logger.info("Build OK")

    solve_popen_opts = command.resolve_solve_popen_opts(
        year=year, day=day, part=part, input_path=input_path
    )
    loguru.logger.info("Running inference ...")
    loguru.logger.info(solve_popen_opts["cmd"])
    proc = subprocess.Popen(
        solve_popen_opts["cmd"],
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=solve_popen_opts["env"],
        cwd=solve_popen_opts["cwd"],
    )

    selector = selectors.DefaultSelector()
    assert proc.stdout is not None
    selector.register(proc.stdout, selectors.EVENT_READ, stdout_handler)

    def handle(timeout: float | None = None) -> None:
        for key, _ in selector.select(timeout):
            key.data(key.fileobj)

    while proc.poll() is None:
        handle()

    # NOTE(vshlenskii): This interval must be enough to read remaining lines.
    timer = threading.Timer(2, _thread.interrupt_main)
    timer.start()
    try:
        parts = resolve_parts(part)
        while len(parsed_solutions) != len(parts):
            handle()
    finally:
        timer.cancel()
    selector.close()

    if (return_code := proc.wait()) != 0:
        selector.close()
        raise subprocess.CalledProcessError(
            return_code,
            solve_popen_opts["cmd"],
            stderr=str(proc.stderr),
        )

    return parsed_solutions
