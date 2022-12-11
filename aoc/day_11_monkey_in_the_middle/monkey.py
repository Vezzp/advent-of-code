from __future__ import annotations

import dataclasses
import operator
from collections import deque
from typing import Callable, Iterable, Iterator

from typing_extensions import Self


@dataclasses.dataclass
class Test:
    divider: int
    pass_monkey_idx: int
    fail_monkey_idx: int

    def apply(self, worry_level: int) -> int:
        out = (
            self.pass_monkey_idx
            if (worry_level % self.divider == 0)
            else self.fail_monkey_idx
        )
        return out


@dataclasses.dataclass
class Op:
    fn: Callable[[int, int], int]
    operand: int | None

    def apply(self, worry_level: int) -> int:
        operand = worry_level if self.operand is None else self.operand
        out = self.fn(worry_level, operand)

        return out


@dataclasses.dataclass
class Monkey:
    idx: int
    items: deque[int]
    op: Op
    test: Test

    def play(self, monkeys: list[Self], relief: Callable[[int], int]) -> None:
        while len(self.items):
            worry_level = self.items.popleft()
            worry_level = self.op.apply(worry_level)
            worry_level = relief(worry_level)  # type: ignore

            next_monkey_idx = self.test.apply(worry_level)
            monkeys[next_monkey_idx].items.append(worry_level)

    @classmethod
    def from_description(cls, spec: Iterable[str]) -> Self:
        spec_it = spec if isinstance(spec, Iterator) else iter(spec)
        move = lambda: next(spec_it).strip()

        idx = int(move().removeprefix("Monkey ").removesuffix(":"))
        items = map(int, move().removeprefix("Starting items: ").split(", "))

        op_, operand_ = move().removeprefix("Operation: new = old ").split()
        match operand_:
            case "old":
                operand = None
            case _:
                operand = int(operand_)

        match op_:
            case "+":
                fn = operator.add
            case "*":
                fn = operator.mul
            case _:
                raise ValueError()

        op = Op(fn, operand)

        divider = int(move().removeprefix("Test: divisible by "))
        pass_monkey_idx = int(move().removeprefix("If true: throw to monkey "))
        fail_monkey_idx = int(move().removeprefix("If false: throw to monkey "))

        test = Test(divider, pass_monkey_idx, fail_monkey_idx)

        out = cls(idx=idx, items=deque(items), op=op, test=test)

        return out
