import _thread
import os
import re
import selectors
import subprocess
import sys
import threading
from pathlib import Path
from typing import Literal, TextIO, TypedDict, cast

import loguru
import typer

from ._langs import LANG_TO_COMMAND, Command
from ._typer import CommonOpts, Part
from ._utils import get_daily_entrypoint, get_daily_present_root, get_lang_path, resolve_parts


class ParsedSolution(TypedDict):
    part: Literal["1", "2"]
    answer: str


SOLUTION_RE = re.compile(r"Part (?P<part>1|2) solution: (?P<answer>\w+)")


def solve_handler(*, ctx: typer.Context, part: Part = None) -> None:
    opts = getattr(ctx, CommonOpts.ATTRNAME, ...)
    assert isinstance(opts, CommonOpts), f"Typer context does not contain expected options: {opts}"

    solve_puzzle(
        command=LANG_TO_COMMAND[opts.lang],
        input_path=get_daily_present_root(year=opts.year, day=opts.day) / "input.txt",
        main_path=get_daily_entrypoint(lang=opts.lang, year=opts.year, day=opts.day),
        part=part,
    )


def solve_puzzle(
    *,
    command: Command,
    main_path: Path,
    input_path: Path,
    part: int | None,
    suppress_stdout: bool = False,
) -> list[ParsedSolution]:
    parsed_solutions: list[ParsedSolution] = []

    cwd = get_lang_path(command.lang)

    # https://gist.github.com/nawatts/e2cdca610463200c12eac2a14efc0bfb
    def stdout_handler(stream: TextIO) -> None:
        line = stream.readline()
        if not suppress_stdout:
            sys.stdout.write(line)
        if (match := SOLUTION_RE.match(line)) is None:
            return
        parsed_solution = cast(ParsedSolution, match.groupdict())
        parsed_solutions.append(parsed_solution)

    if command.build_parts:
        build_args = command.resolve_build_args(main_path)
        loguru.logger.info("Building ...")
        loguru.logger.info(build_args)
        subprocess.check_call(build_args, env=os.environ | (command.build_envs or {}), cwd=cwd)
        loguru.logger.info("Build OK")

    inference_args = command.resolve_inference_args(
        main_path=main_path, input_path=input_path, part=part
    )
    loguru.logger.info("Running inference ...")
    loguru.logger.info(inference_args)
    proc = subprocess.Popen(
        inference_args,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=(command.solve_envs or {}) | os.environ,
        cwd=cwd,
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
            inference_args,
            stderr=str(proc.stderr),
        )

    return parsed_solutions
