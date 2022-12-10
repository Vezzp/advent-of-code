from __future__ import annotations

from typing import TYPE_CHECKING

HEIGHT = 6
WIDTH = 40

if TYPE_CHECKING:
    from aoc.day_10_cathode_ray_tube.cpu import CPU


class CRT:
    def __init__(self) -> None:
        self._ypos = self._xpos = -1
        self._screen = [["."] * WIDTH for _ in range(HEIGHT)]

    def __str__(self) -> str:
        out = "\n".join(map("".join, self._screen))
        return out

    def connect(self, cpu: CPU) -> None:
        self._update_pos()
        self._draw(cpu)

    def _draw(self, cpu: CPU) -> None:
        if abs(self._xpos - cpu.val) <= 1:
            self._screen[self._ypos][self._xpos] = "#"

    def _update_pos(self) -> None:
        match self._ypos:
            case -1:
                self._ypos = self._xpos = 0

            case _:
                xpos = self._xpos
                self._xpos = (xpos + 1) % WIDTH
                self._ypos += (xpos + 1) // WIDTH
