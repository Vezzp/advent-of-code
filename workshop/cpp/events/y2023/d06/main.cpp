#include <algorithm>
#include <charconv>
#include <cmath>
#include <cstdint>
#include <optional>
#include <ranges>
#include <sstream>
#include <string_view>

#include "elf/elf.hpp"

struct QuadricEquation {
  std::int64_t a = 0;
  std::int64_t b = 0;
  std::int64_t c = 0;

  auto
  solve() const noexcept -> std::optional<std::pair<double, double>> {
    auto squared_discriminant = static_cast<std::int64_t>(b) * b - 4 * a * c;
    if (squared_discriminant < 0) {
      return std::nullopt;
    }

    auto discriminant = std::sqrt(squared_discriminant);
    return std::minmax((-b - discriminant) / (2 * a), (-b + discriminant) / (2 * a));
  }
};  // namespace QuadricEquation

struct Race {
  std::int64_t time = 0;
  std::int64_t distance = 0;

  auto
  calc_dist_per_hold_time(int hold_time) const noexcept -> std::int64_t {
    return hold_time * (this->time - hold_time);
  }

  auto
  resolve_distance_trajectory() const noexcept -> QuadricEquation {
    int f1 = this->calc_dist_per_hold_time(1);
    int f2 = this->calc_dist_per_hold_time(2);

    std::int64_t a = (f2 - 2 * f1) / 2;
    std::int64_t b = f1 - a;

    return {.a = a, .b = b, .c = 0};
  }
};

auto
split_row(std::string_view row) {
  return row | std::views::split(' ') | std::views::drop(1) |
         std::views::filter([](auto sv) { return !sv.empty(); });
}

auto
parse_races_from_file(std::string_view filepath) -> std::vector<Race> {
  auto rows = elf::read_file_rows(filepath);

  std::vector<Race> races{};
  for (auto [time_c, distance_c] :
       std::views::zip(split_row(std::move(rows[0])), split_row(std::move(rows[1])))) {
    int time{};
    std::from_chars(time_c.begin(), time_c.end(), time);

    int distance{};
    std::from_chars(distance_c.begin(), distance_c.end(), distance);

    races.emplace_back(time, distance);
  }

  return races;
}

auto
parse_race_from_file_with_broken_kerning(std::string_view filepath) -> Race {
  auto rows = elf::read_file_rows(filepath);

  std::stringstream times_ss, distances_ss;
  for (auto [time_c, distance_c] :
       std::views::zip(split_row(std::move(rows[0])), split_row(std::move(rows[1])))) {
    times_ss << std::string_view(time_c);
    distances_ss << std::string_view(distance_c);
  }

  std::int64_t time{};
  const auto times_s = times_ss.str();
  std::from_chars(times_s.data(), times_s.data() + times_s.size(), time);

  std::int64_t distance{};
  const auto distances_s = distances_ss.str();
  std::from_chars(distances_s.data(), distances_s.data() + distances_s.size(), distance);

  return Race{.time = time, .distance = distance};
}

auto
solve_first_part(std::string_view filepath) -> void {
  const auto races = parse_races_from_file(filepath);

  int solution = 1;
  for (const auto& race : races) {
    int num_wins = 0;
    for (std::int64_t i = 0; i < race.time; ++i) {
      if (race.calc_dist_per_hold_time(i) > race.distance) {
        num_wins++;
      }
    }

    if (num_wins != 0) {
      solution *= num_wins;
    }
  }

  elf::print_solution(1, solution);
}
auto
solve_second_part(std::string_view filepath) -> void {
  const auto race = parse_race_from_file_with_broken_kerning(filepath);

  auto quadric_equation = race.resolve_distance_trajectory();
  quadric_equation.c = -race.distance;

  const auto quadric_equation_solution = quadric_equation.solve();
  auto [lhs, rhs] = quadric_equation_solution.value();
  auto solution = 1 + static_cast<std::int64_t>(std::floor(rhs)) -
                  static_cast<std::int64_t>(std::ceil(lhs));

  elf::print_solution(2, solution);
}

auto
main(const int argc, const char* argv[]) -> int {
  const std::vector<std::string_view> args(
      argv, std::next(argv, static_cast<ptrdiff_t>(argc)));

  const auto config = elf::parse_command_line(args);

  for (const auto part : config.parts) {
    if (part == 1) {
      solve_first_part(config.input);
    } else {
      solve_second_part(config.input);
    };
  }
}
