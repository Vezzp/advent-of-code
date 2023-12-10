#ifndef _JOGTROT_

#define _JOGTROT_

#include <span>
#include <string_view>
#include <vector>

namespace jogtrot {

auto
parse_command_line(std::span<const std::string_view> args) {
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
}

} // namespace jogtrot

#endif