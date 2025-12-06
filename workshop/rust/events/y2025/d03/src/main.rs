use std::cmp::Reverse;

use elf;

fn count_total_battaries_joltage<E>(lines: &[E], n_batteries: usize) -> i64
where
    E: AsRef<str>,
{
    lines
        .iter()
        .map(AsRef::as_ref)
        .map(|line| {
            assert!(line.is_ascii());
            let mut joltage = 0i64;

            let _ = (0..n_batteries)
                .rev()
                .fold(0usize, |search_range_start, magnitude| {
                    let digit_idx = (search_range_start..line.len() - magnitude)
                        .min_by_key(|&idx| Reverse(line.as_bytes()[idx]))
                        .expect("Non-empty search slice");

                    joltage +=
                        10i64.pow(magnitude as u32) * i64::from(line.as_bytes()[digit_idx] - b'0');

                    digit_idx + 1
                });

            joltage
        })
        .sum()
}

fn solve_part_1<E: AsRef<str>>(lines: &[E]) -> String {
    count_total_battaries_joltage(lines, 2).to_string()
}

fn solve_part_2<E: AsRef<str>>(lines: &[E]) -> String {
    count_total_battaries_joltage(lines, 12).to_string()
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
