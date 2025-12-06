use elf;

fn solve_part_1<E: AsRef<str>>(lines: &[E]) -> String {
    return count_invalid_ids(lines, check_invalid_id).to_string();

    fn check_invalid_id(id: i64) -> bool {
        let candidate_id = id.to_string();
        check_string_k_repeatable(candidate_id.as_str(), candidate_id.len() / 2)
    }
}

fn solve_part_2<E: AsRef<str>>(lines: &[E]) -> String {
    return count_invalid_ids(lines, check_invalid_id).to_string();

    fn check_invalid_id(id: i64) -> bool {
        let id = id.to_string();
        (1..=id.len() / 2)
            .map(|k| check_string_k_repeatable(id.as_str(), k))
            .any(std::convert::identity)
    }
}

fn count_invalid_ids<E, V>(lines: &[E], invalid_id_checker: V) -> i64
where
    E: AsRef<str>,
    V: Fn(i64) -> bool,
{
    lines[0]
        .as_ref()
        .split(",")
        .map(|range| {
            let (lhs, rhs) = range
                .split_once("-")
                .expect("Cannot split range into lhs/rhs");
            let lhs = lhs.parse::<i64>().expect("Cannot parse range lhs");
            let rhs = rhs.parse::<i64>().expect("Cannot parse range rhs");
            assert!(lhs <= rhs, "Range lhs {lhs} is greater than rhs = {rhs}");

            (lhs..=rhs).fold(0i64, |acc, id| acc + id * i64::from(invalid_id_checker(id)))
        })
        .sum()
}

fn check_string_k_repeatable(s: &str, k: usize) -> bool {
    const WINDOW_SIZE: usize = 3;

    (k != 0)
        && (s.len() / k != 0)
        && (s.len() % k == 0)
        && (0..=s.len())
            .step_by(k)
            .collect::<Vec<_>>()
            .windows(WINDOW_SIZE)
            .map(|window| {
                let [lhs, mhs, rhs]: [usize; WINDOW_SIZE] = window
                    .try_into()
                    .expect("Cannot cast window to {WINDOW_SIZE}-tuple");
                s[lhs..mhs] == s[mhs..rhs]
            })
            .all(std::convert::identity)
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
