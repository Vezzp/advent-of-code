use std::ops::{IndexMut, Range};

use elf;

#[derive(Debug)]
enum Op {
    Add,
    Mul,
}

impl Op {
    fn identity(&self) -> i64 {
        match *self {
            Op::Add => 0i64,
            Op::Mul => 1i64,
        }
    }

    fn apply(&self, lhs: i64, rhs: i64) -> i64 {
        match *self {
            Op::Add => lhs + rhs,
            Op::Mul => lhs * rhs,
        }
    }

    fn apply_inplace(&self, lhs: &mut i64, rhs: i64) -> () {
        *lhs = self.apply(*lhs, rhs)
    }
}

fn solve_part_1<E: AsRef<str>>(lines: &[E]) -> String {
    let (columns, ops) = parse_footer(lines);
    let mut accumulators = ops.iter().map(Op::identity).collect::<Vec<_>>();

    columns.iter().enumerate().for_each(|(idx, column)| {
        lines[0..lines.len() - 1].iter().for_each(|line| {
            let number = line.as_ref()[column.clone()]
                .trim()
                .parse::<i64>()
                .expect("Cannot parse number from digits");

            ops[idx].apply_inplace(accumulators.index_mut(idx), number);
        });
    });

    accumulators.iter().sum::<i64>().to_string()
}

fn solve_part_2<E: AsRef<str>>(lines: &[E]) -> String {
    let (columns, ops) = parse_footer(lines);
    let mut accumulators = ops.iter().map(Op::identity).collect::<Vec<_>>();

    let mut digits = Vec::<u8>::with_capacity(lines.len() - 1);
    columns.iter().enumerate().for_each(|(idx, column)| {
        for ch_idx in column.clone() {
            digits.clear();
            lines[0..lines.len() - 1]
                .iter()
                .map(|line| line.as_ref().as_bytes()[ch_idx])
                .filter(|&ch| ch != b' ')
                .for_each(|digit| digits.push(digit));

            let number = std::str::from_utf8(&digits)
                .expect("Unconstructive number string")
                .parse::<i64>()
                .expect("Cannot parse number from digits");

            ops[idx].apply_inplace(accumulators.index_mut(idx), number);
        }
    });

    accumulators.iter().sum::<i64>().to_string()
}

fn parse_footer<E: AsRef<str>>(lines: &[E]) -> (Vec<Range<usize>>, Vec<Op>) {
    let line = lines.last().expect("Empty input").as_ref();
    let mut columns: Vec<Range<usize>> = vec![];
    let mut ops: Vec<Op> = vec![];
    line.chars().enumerate().for_each(|(idx, ch)| {
        if ch.is_whitespace() {
            return;
        }

        if let Some(range) = columns.last_mut() {
            range.end = idx - 1;
        }

        columns.push(idx..line.len());
        ops.push(match ch {
            '+' => Op::Add,
            '*' => Op::Mul,
            _ => panic!("Not an arithmetic operation"),
        });
    });

    (columns, ops)
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
