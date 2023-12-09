from __future__ import annotations

import itertools
import math
from typing import Generator, Iterable, Sized, TypeVar

_T = TypeVar("_T")


def chunked(lst: Iterable[_T], chunk_size: int) -> Generator[Iterable[_T], None, None]:
    if not isinstance(lst, Sized):
        lst = list(lst)

    start_idx = 0
    for _ in range(math.ceil(len(lst) / chunk_size)):
        yield itertools.islice(lst, start_idx, (start_idx := start_idx + chunk_size))
