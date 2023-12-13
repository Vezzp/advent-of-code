#ifndef _JOGTROT_

#define _JOGTROT_

#include "fmt/core.h"
#include <concepts>
#include <exception>
#include <fstream>
#include <ranges>
#include <span>
#include <string>
#include <string_view>
#include <vector>

namespace jogtrot {

struct CommandLineConfig {
  std::vector<int> parts;
  std::string input;
};

auto
read_file_rows(std::string_view filepath) -> std::vector<std::string> {
  std::ifstream file(filepath);
  if (!file.is_open()) {
    throw std::runtime_error(fmt::format("Cannot open file {}\n", filepath));
  }

  std::vector<std::string> rows;
  std::string row;
  while (std::getline(file, row)) {
    rows.push_back(std::move(row));
  }

  return rows;
}

template <typename T>
requires std::integral<T> || std::is_convertible_v<T, std::string_view>
auto
print_solution(int part, const T solution) -> void {
  fmt::print("Part {} solution: {}\n", part, solution);
}

auto
parse_command_line(std::span<const std::string_view> args) -> CommandLineConfig {
  std::string_view part, input;

  for (std::size_t i = 1; i < args.size(); i++) {
    if (args[i] == "-p") {
      part = args[i + 1];
    } else if (args[i] == "-i") {
      input = args[i + 1];
    }
  }

  std::vector<int> parts;
  parts.reserve(2);

  if (part == "1") {
    parts = {1};
  } else if (part == "2") {
    parts = {2};
  } else {
    parts = {1, 2};
  }

  if (input.empty()) {
    input = "./input.txt";
  }

  return CommandLineConfig{parts, std::string{input}};
}

} // namespace jogtrot

#endif