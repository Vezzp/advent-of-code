from __future__ import annotations

from collections import deque
from typing import Any, Callable, Iterable


def consume(it: Iterable[Any]) -> None:
    deque(it, maxlen=0)


def applymap(fn: Callable, it: Iterable[Any]) -> None:
    consume(map(fn, it))
