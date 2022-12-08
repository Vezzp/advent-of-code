from __future__ import annotations

import enum
import functools
import itertools
from typing import Generator

from typing_extensions import Self, TypedDict, Unpack


class FSObjectType(enum.Enum):
    DIR = enum.auto()
    FILE = enum.auto()


class FSObjectInitParams(TypedDict):
    name: str
    parent: Dir | None


class FSObject:
    fstype: FSObjectType
    size: int

    def __init_subclass__(cls, fstype: FSObjectType) -> None:
        super().__init_subclass__()
        cls.fstype = fstype

    def __init__(self, **kwargs: Unpack[FSObjectInitParams]) -> None:
        self.name = kwargs["name"]
        self.parent = kwargs["parent"]
        self._is_protected = False

    def __repr__(self) -> str:
        out = f"{self.name} ({self.fstype.name})"
        return out

    def is_dir(self) -> bool:
        return self.fstype is FSObjectType.DIR

    def is_file(self) -> bool:
        return self.fstype is FSObjectType.FILE

    def protect(self) -> None:
        self._is_protected = True

    def unprotect(self) -> None:
        self._is_protected = False



    @property
    def root(self) -> Self:
        out = self
        while self.parent:
            out = self.parent
        return out


class File(FSObject, fstype=FSObjectType.FILE):
    def __init__(self, *, size: int, **kwargs: Unpack[FSObjectInitParams]) -> None:
        super().__init__(**kwargs)
        self.size = size

    def __repr__(self) -> str:
        out = f"{self.name} ({self.fstype.name}, size={self.size})"
        return out


class Dir(FSObject, fstype=FSObjectType.DIR):
    def __init__(self, **kwargs: Unpack[FSObjectInitParams]) -> None:
        super().__init__(**kwargs)

        self._is_protected = False
        self._cached_size = None
        self._children: dict[str, FSObject] = {}

    def protect(self) -> None:
        for child in self.iterdir():
            child.protect()
        self._cached_size = None
        super().protect()

    def unprotect(self) -> None:
        self._is_protected = False
        self._cached_size = None
        super().unprotect()

    def touch(self, name: str, size: int) -> File:
        self.unprotect()
        self._children[name] = (out := File(size=size, name=name, parent=self))
        return out

    def mkdir(self, name: str) -> Self:
        self.unprotect()
        self._children[name] = (out := Dir(name=name, parent=self))
        return out

    @property
    def size(self) -> int:
        assert self._is_protected

        if (out := self._cached_size) is None:
            out = sum(child.size for child in self.iterdir())

        return out

    def riterdir(self) -> Generator[FSObject, None, None]:
        for child in self.iterdir():
            yield child
            if isinstance(child, Dir):
                yield from child.riterdir()

    def iterdir(self) -> Generator[FSObject, None, None]:
        yield from self._children.values()

    def tree(self, indent: int = 2, sep: str = " ") -> str:
        out = "\n".join(
            (f"{level * indent * sep}- {fso}" for fso, level in _tree(self))
        )
        return out

    def cd(self, dirname: str) -> Self:
        match dirname:
            case "..":
                assert self.parent is not None
                return self.parent

            case "/":
                return self.root

            case _:
                if (out := self._children.get(dirname)) is None:
                    self._children[dirname] = (out := Dir(name=dirname, parent=self))

                assert isinstance(out, Dir)

                return out

    @classmethod
    def empty_filesystem(cls) -> Self:
        out = cls(name="/", parent=None)
        return out


def _tree(fso: FSObject, level: int = 0) -> Generator[tuple[FSObject, int], None, None]:
    yield (fso, level)
    if isinstance(fso, Dir):
        yield from itertools.chain.from_iterable(
            map(functools.partial(_tree, level=level + 1), fso.iterdir())
        )
