use std::path::Path;

use elf;

fn solve<P, V>(path: P, invalid_id_checker: V) -> i64
where
    P: AsRef<Path>,
    V: Fn(i64) -> bool,
{
    elf::read_file_rows(&path)[0]
        .split(",")
        .map(|range| {
            let (lhs, rhs) = range
                .split_once("-")
                .expect("Cannot split range into lhs/rhs");
            let lhs = lhs.parse::<i64>().expect("Cannot parse range lhs");
            let rhs = rhs.parse::<i64>().expect("Cannot parse range rhs");
            assert!(lhs <= rhs, "Range lhs {lhs} is greater than rhs = {rhs}");

            (lhs..=rhs).fold(0i64, |acc, id| acc + id * invalid_id_checker(id) as i64)
        })
        .sum()
}

fn solve_first_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let solution: i64 = solve(&path, check_id_invalid);
    elf::print_solution(1, &solution);

    fn check_id_invalid(id: i64) -> bool {
        let candidate_id = id.to_string();
        check_id_k_invalid(candidate_id.as_str(), 2)
    }
}

fn solve_second_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let solution: i64 = solve(&path, check_id_invalid);
    elf::print_solution(2, &solution);

    fn check_id_invalid(id: i64) -> bool {
        let id = id.to_string();
        (1..=id.len() / 2)
            .map(|k| check_id_k_invalid(id.as_str(), k))
            .any(std::convert::identity)
    }
}

fn check_id_k_invalid(id: &str, k: usize) -> bool {
    const WINDOW_SIZE: usize = 3;

    let size = id.len();
    (size % k == 0)
        && (0..=size)
            .step_by(k)
            .collect::<Vec<_>>()
            .windows(WINDOW_SIZE)
            .map(|window| {
                let [lhs, mhs, rhs]: [usize; WINDOW_SIZE] = window
                    .try_into()
                    .expect("Cannot cast window to {WINDOW_SIZE}-tuple");
                id[lhs..mhs] == id[mhs..rhs]
            })
            .all(std::convert::identity)
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
