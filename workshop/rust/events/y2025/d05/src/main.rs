use std::ops::RangeInclusive;

use elf;

fn parse_input<E: AsRef<str>>(lines: &[E]) -> (Vec<RangeInclusive<i64>>, Vec<i64>) {
    let mut section_idx = 0;
    let mut id_ranges: Vec<RangeInclusive<i64>> = vec![];
    let mut ids: Vec<i64> = vec![];
    for line in lines {
        let line = line.as_ref().trim();
        if line.is_empty() {
            section_idx += 1;
            continue;
        }

        match section_idx {
            0 => {
                let (lhs, rhs) = line
                    .split_once("-")
                    .expect("Stringified range does not contain expected delimeter");

                let id_range = RangeInclusive::new(
                    lhs.parse::<i64>().expect("Invalid range start"),
                    rhs.parse::<i64>().expect("Invalid range end"),
                );
                assert!(
                    id_range.start() <= id_range.end(),
                    "Range start exceeded its end"
                );

                id_ranges.push(id_range);
            }
            1 => {
                ids.push(line.parse::<i64>().expect("Unparsable ID"));
            }
            _ => unreachable!("Unexpected input section for parsing"),
        }
    }

    (id_ranges, ids)
}

fn solve_part_1<E: AsRef<str>>(lines: &[E]) -> String {
    let (id_ranges, ids) = parse_input(lines);
    ids.iter()
        .map(|id| {
            id_ranges
                .iter()
                .map(|id_range| id_range.contains(&id))
                .any(std::convert::identity)
        })
        .map(i64::from)
        .sum::<i64>()
        .to_string()
}

fn solve_part_2<E: AsRef<str>>(lines: &[E]) -> impl std::fmt::Display {
    let (mut id_ranges, _) = parse_input(lines);

    id_ranges.sort_unstable_by_key(|id_range| *id_range.start());

    let merged_id_ranges = {
        let mut merged_id_ranges = vec![];
        for id_range in id_ranges.iter() {
            match merged_id_ranges.last_mut() {
                None => {
                    merged_id_ranges.push(id_range.clone());
                }
                Some(last_id_range) => {
                    if last_id_range.end() >= id_range.start() {
                        *last_id_range = RangeInclusive::new(
                            (*last_id_range.start()).min(*id_range.start()),
                            (*last_id_range.end()).max(*id_range.end()),
                        );
                    } else {
                        merged_id_ranges.push(id_range.clone());
                    }
                }
            }
        }

        merged_id_ranges
    };

    merged_id_ranges
        .iter()
        .map(|id_range| (id_range.end() - id_range.start() + 1) as i64)
        .sum::<i64>()
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
