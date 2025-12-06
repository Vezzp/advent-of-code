use elf;

fn solve_part_1<E: AsRef<str>>(lines: &[E]) -> String {
    _ = lines;
    "Unimplemented".to_string()
}

fn solve_part_2<E: AsRef<str>>(lines: &[E]) -> String {
    _ = lines;
    "Unimplemented".to_string()
}

fn main() {
    let config = elf::CommandLineConfig::from_args(&std::env::args().collect::<Vec<_>>());
    let lines = elf::read_file_lines(&config.input_path);
    for part in config.parts {
        match part {
            1 => elf::print_solution(part, solve_part_1(&lines)),
            2 => elf::print_solution(part, solve_part_2(&lines)),
            _ => unreachable!(),
        }
    }
}
