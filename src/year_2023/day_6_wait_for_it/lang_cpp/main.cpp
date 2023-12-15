// https://stackoverflow.com/a/66946587
#define FMT_HEADER_ONLY

#include "jogtrot/jogtrot.hpp"
#include <charconv>
#include <fmt/core.h>
#include <fmt/ranges.h>
#include <ranges>
#include <string_view>
#include <vector>

struct Race {
  int time = 0;
  int distance = 0;
};

auto
parse_races_from_file(std::string_view filepath) -> std::vector<Race> {
  auto splitter = [](std::string_view input) -> auto{
    return input | std::views::split(' ') | std::views::drop(1) |
           std::views::filter([](auto sv) { return !sv.empty(); });
  };
  auto rows = jogtrot::read_file_rows(filepath);

  std::vector<Race> races{};
  for (auto [time_c, distance_c] :
       std::views::zip(splitter(std::move(rows[0])), splitter(std::move(rows[1])))) {

    int time{}, distance{};
    std::from_chars(time_c.begin(), time_c.end(), time);
    std::from_chars(distance_c.begin(), distance_c.end(), distance);

    races.emplace_back(time, distance);
  }

  return races;
}

auto
solve_first_part(std::string_view filepath) -> void {
  const auto races = parse_races_from_file(filepath);

  int solution = 1;
  for (const auto& race : races) {
    int num_wins = 0;
    for (int hold_time : std::views::iota(1, 1 + race.time)) {
      if (hold_time * (race.time - hold_time) > race.distance) {
        num_wins++;
      }
    }

    if (num_wins != 0) {
      solution *= num_wins;
    }
  }

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