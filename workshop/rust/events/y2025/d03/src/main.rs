use std::{cmp::Reverse, path::Path};

use elf;

fn solve<P>(path: P, n_batteries: usize) -> i64
where
    P: AsRef<Path>,
{
    elf::read_file_rows(&path)
        .iter()
        .map(|line| {
            assert!(line.is_ascii());

            let (_, joltage) =
                (0..n_batteries)
                    .rev()
                    .fold((0usize, 0i64), |(start_pos, joltage), magnitude| {
                        let digit_pos = (start_pos..line.len() - magnitude)
                            .min_by_key(|&pos| Reverse(line.as_bytes()[pos]))
                            .expect("Non-empty search slice");
                        let digit = (line.as_bytes()[digit_pos] - b'0') as i64;

                        (digit_pos + 1, joltage + 10i64.pow(magnitude as u32) * digit)
                    });

            joltage
        })
        .sum()
}

fn solve_first_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let solution = solve(&path, 2);
    elf::print_solution(1, &solution);
}

fn solve_second_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let solution = solve(&path, 12);
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
