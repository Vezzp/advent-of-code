#include <cctype>
#include <span>
#include <sstream>
#include <string_view>
#include <unordered_map>
#include <vector>

#include "elf/elf.hpp"

const std::unordered_map<std::string_view, std::string_view> SPELL_TO_DIGIT = {
    {"one", "1"}, {"two", "2"},   {"three", "3"}, {"four", "4"}, {"five", "5"},
    {"six", "6"}, {"seven", "7"}, {"eight", "8"}, {"nine", "9"},
};

auto resolve_string_without_spelled_digits(std::string &&str) -> std::string {
  std::stringstream ss;
  const auto view = std::string_view{str};
  for (std::size_t idx = 0; idx < str.size(); ++idx) {
    const auto sub_view = view.substr(idx);
    if (std::isdigit(sub_view.front())) {
      ss << sub_view.front();
      continue;
    }

    for (const auto &[spell, digit] : SPELL_TO_DIGIT) {
      if (sub_view.starts_with(spell)) {
        ss << digit;
        break;
      }
    }
  }

  return ss.str();
};

auto solve(std::span<std::string> rows) -> int {
  int out = 0;
  for (const auto &row : rows) {
    int lhs, rhs;
    lhs = rhs = -1;

    for (const auto ch : row) {
      if (!std::isdigit(ch)) {
        continue;
      }
      if (lhs == -1) {
        lhs = static_cast<int>(ch - '0');
      }
      rhs = static_cast<int>(ch - '0');
    }

    out += 10 * lhs + rhs;
  }

  return out;
}

auto solve_first_part(std::string_view filepath) -> void {
  auto rows = elf::read_file_rows(filepath);
  const auto solution = solve(rows);
  elf::print_solution(1, solution);
}
auto solve_second_part(std::string_view filepath) -> void {
  auto rows = elf::read_file_rows(filepath);
  for (std::size_t idx = 0; idx < rows.size(); ++idx) {
    rows[idx] = resolve_string_without_spelled_digits(std::move(rows[idx]));
  }
  const auto solution = solve(rows);
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
    };
  }
}
