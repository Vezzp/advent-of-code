// https://stackoverflow.com/a/66946587

#include <cassert>
#include <string_view>
#include <utility>
#include <vector>
#include <fmt/core.h>

#include "elf/elf.hpp"

auto solve_first_part(std::string_view filepath) -> void {
  std::string solution =
      fmt::format("Unimplemented. No solution for {}", filepath);
  elf::print_solution(1, solution);
}

auto solve_second_part(std::string_view filepath) -> void {
  std::string solution =
      fmt::format("Unimplemented. No solution for {}", filepath);
  elf::print_solution(2, solution);
}

auto main(const int argc, const char *argv[]) -> int {
  const std::vector<std::string_view> args(
      argv, std::next(argv, static_cast<ptrdiff_t>(argc)));

  const auto config = elf::parse_command_line(args);

  for (const auto part : config.parts) {
    if (part == 1) {
      solve_first_part(config.input);
    } else if (part == 2) {
      solve_second_part(config.input);
    } else {
      std::unreachable();
    };
  }
}
