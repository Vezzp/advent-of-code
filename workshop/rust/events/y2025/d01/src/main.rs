use elf;

#[derive(Debug)]
enum Rotation {
    L(i32),
    R(i32),
}

impl Rotation {
    fn value(&self) -> i32 {
        match *self {
            Rotation::L(value) | Rotation::R(value) => value,
        }
    }

    fn sign(&self) -> i32 {
        match *self {
            Rotation::L(_) => -1,
            Rotation::R(_) => 1,
        }
    }
}

impl TryFrom<&str> for Rotation {
    type Error = &'static str;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        let (direction, value) = s.split_at(1);
        let value = value.parse::<i32>().expect("Cannot parse angle");
        match direction {
            "L" => Ok(Rotation::L(value)),
            "R" => Ok(Rotation::R(value)),
            _ => Err("Invalid rotation direction"),
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
        self.position = (self.position + rotation.value() * rotation.sign()).rem_euclid(self.size);
    }
}

fn solve_part_1<E: AsRef<str>>(lines: &[E]) -> String {
    let mut dial = Dial::default();
    lines
        .iter()
        .map(|line| {
            let rotation = Rotation::try_from(line.as_ref()).expect("Cannot parse rotation");
            dial.rotate(&rotation);
            i32::from(dial.position == 0)
        })
        .sum::<i32>()
        .to_string()
}

fn solve_part_2<E: AsRef<str>>(lines: &[E]) -> String {
    let mut dial = Dial::default();
    lines
        .iter()
        .map(|line| {
            let rotation = Rotation::try_from(line.as_ref()).expect("Cannot parse rotation");

            let n_clicks = {
                let right_rotatible_position = match &rotation {
                    Rotation::R(_) => dial.position,
                    Rotation::L(_) => (dial.size - dial.position) % dial.size,
                };
                (right_rotatible_position + rotation.value()) / dial.size
            };

            dial.rotate(&rotation);

            n_clicks
        })
        .sum::<i32>()
        .to_string()
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
