import itertools
from collections import defaultdict
from pathlib import Path
from typing import assert_never

import elf

type Rules = dict[int, set[int]]
type Update = list[int]
type Updates = list[Update]


def parse_data(__p: Path, /) -> tuple[Rules, Updates]:
    lines = elf.read_file_rows(__p)
    sep_idx = lines.index("")

    rules: Rules = defaultdict(set)
    for line in itertools.islice(lines, sep_idx):
        lhs, rhs = map(int, line.strip().split("|"))
        rules[lhs].add(rhs)

    updates: Updates = [
        list(map(int, line.strip().split(",")))
        for line in itertools.islice(lines, sep_idx + 1, None)
    ]

    return rules, updates


def check_update_satisfy_rules(update: Update, rules: Rules) -> bool:
    for prev, next in itertools.combinations(range(len(update)), 2):
        if update[next] not in rules[update[prev]]:
            return False
    return True


def transform_update_to_satisfy_rules(update: Update, rules: Rules) -> Update:
    new_rules: Rules = {v: rules[v].intersection(update) for v in update}
    new_update = sorted(new_rules, key=lambda v: len(new_rules[v]), reverse=True)
    assert check_update_satisfy_rules(new_update, rules)
    return new_update


def solve_first_part(__p: Path, /) -> None:
    rules, updates = parse_data(__p)

    solution = 0
    for update in updates:
        if check_update_satisfy_rules(update, rules):
            solution += update[len(update) // 2]

    elf.print_solution(1, solution)


def solve_second_part(__p: Path, /) -> None:
    rules, updates = parse_data(__p)

    solution = 0
    for new_update in updates:
        if check_update_satisfy_rules(new_update, rules):
            continue
        new_update = transform_update_to_satisfy_rules(new_update, rules)
        solution += new_update[len(new_update) // 2]

    elf.print_solution(2, solution)


def main() -> None:
    parts, input = elf.parse_command_line()
    for part in parts:
        match part:
            case 1:
                solve_first_part(input)
            case 2:
                solve_second_part(input)
            case _:
                assert_never(part)


if __name__ == "__main__":
    main()
