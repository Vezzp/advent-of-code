import heapq
import elf


def solve_first_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    max_calories = 0
    current_calories = 0

    for line in lines:
        if line.strip() == "":
            max_calories = max(current_calories, max_calories)
            current_calories = 0
        else:
            current_calories += int(line.strip())

    # Don't forget the last elf
    max_calories = max(current_calories, max_calories)
    elf.print_solution(1, max_calories)


def solve_second_part(filepath: str) -> None:
    lines = elf.read_file_rows(filepath)
    # Keep track of top 3 calorie counts using a min heap
    heap = []
    current_calories = 0

    for line in lines:
        if line.strip() == "":
            if len(heap) >= 3:
                heapq.heappushpop(heap, current_calories)
            else:
                heapq.heappush(heap, current_calories)
            current_calories = 0
        else:
            current_calories += int(line.strip())

    # Don't forget the last elf
    if len(heap) >= 3:
        heapq.heappushpop(heap, current_calories)
    else:
        heapq.heappush(heap, current_calories)

    elf.print_solution(2, sum(heap))


def main():
    parts, input_path = elf.parse_command_line()

    for part in parts:
        if part == 1:
            solve_first_part(input_path)
        elif part == 2:
            solve_second_part(input_path)


if __name__ == "__main__":
    main()
