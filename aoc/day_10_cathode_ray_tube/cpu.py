from __future__ import annotations

import abc
import dataclasses
from typing import Iterator


@dataclasses.dataclass
class Op(abc.ABC):
    @abc.abstractmethod
    def run(self, cpu: CPU) -> Iterator[CPU]:
        ...


@dataclasses.dataclass
class Noop(Op):
    def run(self, cpu: CPU) -> Iterator[CPU]:
        cpu.clock += 1
        yield cpu


@dataclasses.dataclass
class Addx(Noop):
    val: int

    def run(self, cpu: CPU) -> Iterator[CPU]:
        yield from Noop.run(self, cpu)
        yield from Noop.run(self, cpu)
        cpu.val += self.val


@dataclasses.dataclass
class CPU:
    val: int = 1
    clock: int = 0
