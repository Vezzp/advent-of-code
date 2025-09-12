from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional
import elf


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    parent: Optional[Directory] = None
    subdirs: Dict[str, Directory] = field(default_factory=dict)
    files: Dict[str, File] = field(default_factory=dict)

    @property
    def size(self) -> int:
        total = sum(f.size for f in self.files.values())
        total += sum(d.size for d in self.subdirs.values())
        return total

    def all_dirs(self):
        yield self
        for subdir in self.subdirs.values():
            yield from subdir.all_dirs()


def parse_filesystem(lines: list[str]) -> Directory:
    root = Directory("/")
    current = root

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("$ cd"):
            path = line[5:]
            if path == "/":
                current = root
            elif path == "..":
                if current.parent:
                    current = current.parent
            else:
                if path not in current.subdirs:
                    current.subdirs[path] = Directory(path, current)
                current = current.subdirs[path]
        elif line.startswith("$ ls"):
            continue
        else:
            parts = line.split()
            if parts[0] == "dir":
                name = parts[1]
                if name not in current.subdirs:
                    current.subdirs[name] = Directory(name, current)
            else:
                size = int(parts[0])
                name = parts[1]
                current.files[name] = File(name, size)

    return root


def solve_first_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    root = parse_filesystem(lines)

    MAX_DIR_SIZE = 100_000
    total = 0

    for dir_ in root.all_dirs():
        dir_size = dir_.size
        if dir_size <= MAX_DIR_SIZE:
            total += dir_size

    elf.print_solution(1, total)


def solve_second_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    root = parse_filesystem(lines)

    TOTAL_DISK_SPACE = 70_000_000
    REQUIRED_SPACE = 30_000_000

    used_space = root.size
    free_space = TOTAL_DISK_SPACE - used_space
    need_to_free = REQUIRED_SPACE - free_space

    if need_to_free <= 0:
        elf.print_solution(2, 0)
        return

    candidates = []
    for dir_ in root.all_dirs():
        if dir_.size >= need_to_free:
            candidates.append(dir_.size)

    elf.print_solution(2, min(candidates) if candidates else 0)


def main():
    parts, input_path = elf.parse_command_line()

    for part in parts:
        if part == 1:
            solve_first_part(input_path)
        elif part == 2:
            solve_second_part(input_path)


if __name__ == "__main__":
    main()
