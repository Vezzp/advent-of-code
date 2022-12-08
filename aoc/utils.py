from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from typing import Callable, Generic, TypeVar, cast

from typing_extensions import NamedTuple, Self

_T = TypeVar("_T")


class TestInput(NamedTuple, Generic[_T]):
    stream: io.StringIO
    etalon: _T

    @classmethod
    def construct(cls, src: io.StringIO | str | Path, etalon: _T) -> Self:
        if isinstance(src, Path):
            src = src.read_text()

        if isinstance(src, str):
            src = io.StringIO(src)

        out = cls(stream=src, etalon=etalon)

        return out


def run_tests(
    solver: Callable[[io.StringIO], _T],
    *variants: tuple[io.StringIO | str | Path, _T],
) -> None:
    test_inputs = [
        cast(TestInput[_T], TestInput.construct(*variant)) for variant in variants
    ]

    class TestCase(unittest.TestCase):
        def test(self) -> None:
            for stream, etalon in test_inputs:
                with self.subTest():
                    self.assertEqual(solver(stream), etalon)

    test_runner = unittest.TextTestRunner(stream=sys.stdout)
    test_runner.run(unittest.makeSuite(TestCase))
