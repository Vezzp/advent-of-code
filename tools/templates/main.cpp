// https://stackoverflow.com/a/66946587
#define FMT_HEADER_ONLY

#include "fmt/ranges.h"
#include "jogtrot/jogtrot.hpp"
#include <string_view>
#include <vector>

int
main(const int argc, const char* argv[]) {
  std::vector<std::string_view> args(
      argv, std::next(argv, static_cast<ptrdiff_t>(argc))
  );

  fmt::print("{}\n", args);
}