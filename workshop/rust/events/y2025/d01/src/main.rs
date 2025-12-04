use std::{
    ops::{Add, Div},
    path::Path,
};

use elf;

#[derive(Debug)]
enum Rotation {
    Left(i32),
    Right(i32),
}

impl Rotation {
    fn angle(&self) -> i32 {
        match *self {
            Rotation::Left(angle) => angle,
            Rotation::Right(angle) => angle,
        }
    }
}

impl TryFrom<&str> for Rotation {
    type Error = &'static str;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        let angle: i32 = s[1..].parse().map_err(|_| "cannot parse int")?;
        match &s[0..1] {
            "L" => Ok(Rotation::Left(angle)),
            "R" => Ok(Rotation::Right(angle)),
            _ => Err("cannot parse rotation direction"),
        }
    }
}

impl From<&Rotation> for i32 {
    fn from(rotation: &Rotation) -> i32 {
        match *rotation {
            Rotation::Left(angle) => -angle,
            Rotation::Right(angle) => angle,
        }
    }
}

#[derive(Debug)]
struct Dial {
    position: i32,
    size: i32,
}

impl Default for Dial {
    fn default() -> Self {
        Self {
            position: 50,
            size: 100,
        }
    }
}

impl Dial {
    fn rotate(&mut self, rotation: &Rotation) {
        self.position = (self.position + i32::from(rotation)).rem_euclid(self.size);
    }

    fn rotate_with_clicks(&mut self, rotation: &Rotation) -> i32 {
        let n_cliks = match rotation {
            Rotation::Right(_) => self.position,
            Rotation::Left(_) => (self.size - self.position) % self.size,
        }
        .add(rotation.angle())
        .div(self.size);
        self.rotate(rotation);
        n_cliks
    }
}

fn solve_first_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let mut solution: i32 = 0;
    let mut dial = Dial::default();
    for line in elf::read_file_rows(&path) {
        let rotation = Rotation::try_from(line.as_str()).expect("Cannot parse rotation");
        dial.rotate(&rotation);
        solution += (dial.position == 0) as i32;
    }
    elf::print_solution(1, &solution);
}

fn solve_second_part<P>(path: P) -> ()
where
    P: AsRef<Path>,
{
    let mut solution: i32 = 0;
    let mut dial = Dial::default();
    for line in elf::read_file_rows(&path) {
        let rotation = Rotation::try_from(line.as_str()).expect("Cannot parse rotation");
        let n_clicks = dial.rotate_with_clicks(&rotation);
        solution += n_clicks;
    }
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
