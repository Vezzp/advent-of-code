// https://stackoverflow.com/a/66946587
#define FMT_HEADER_ONLY

#include "fmt/ranges.h"
#include "jogtrot/jogtrot.hpp"
#include <string_view>
#include <vector>

auto
solve_first_part(std::string_view filepath) -> void {
  std::string solution = fmt::format("Unimplemented. No solution for {}", filepath);
  jogtrot::print_solution(1, solution);
}
auto
solve_second_part(std::string_view filepath) -> void {
  std::string solution = fmt::format("Unimplemented. No solution for {}", filepath);
  jogtrot::print_solution(2, solution);
}

auto
main(const int argc, const char* argv[]) -> int {
  const std::vector<std::string_view> args(
      argv, std::next(argv, static_cast<ptrdiff_t>(argc))
  );

  const auto config = jogtrot::parse_command_line(args);

  for (const auto part : config.parts) {
    if (part == 1) {
      solve_first_part(config.input);
    } else {
      solve_second_part(config.input);
    };
  }
}