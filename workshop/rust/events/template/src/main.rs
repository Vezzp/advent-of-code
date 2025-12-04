use std::path::Path;

use elf;

fn solve_first_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let solution = format!("Unimplemented. No solution for {:?}", path.as_ref());
    elf::print_solution(1, &solution);
}

fn solve_second_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let solution = format!("Unimplemented. No solution for {:?}", path.as_ref());
    elf::print_solution(2, &solution);
}

fn main() {
    let args = std::env::args().collect::<Vec<_>>();
    let config =
        elf::CommandLineConfig::from_args(&args.iter().map(String::as_str).collect::<Vec<_>>());
    for part in config.parts {
        match part {
            1 => solve_first_part(&config.input_path),
            2 => solve_second_part(&config.input_path),
            _ => unreachable!(),
        }
    }
}
